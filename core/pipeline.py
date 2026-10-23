"""Project pipeline: incremental ingestion, conversational query rewriting and cited answers."""
from __future__ import annotations
import hashlib, json, logging, os, time
import re
from pathlib import Path
from core.config import ProjectConfig
from core.models import Document, Citation, QueryResponse
from chunkers import make_chunker
from embedders import make_embedder
from stores.chroma import ChromaStore
from stores.qdrant import QdrantStore
from retrievers.hybrid import HybridRetriever
from llms import make_llm
from loaders import load_source
log=logging.getLogger("rag")
def _matches_any(text:str,patterns:list[str])->bool:
    return any(re.search(pattern,text,re.I) for pattern in patterns)

def _safe_context(value:dict,allowed_fields:list[str],private_patterns:list[str])->dict:
    """Keep only customer-context fields and remove internal/sensitive details."""
    safe={}
    for key in allowed_fields:
        item=value.get(key)
        if item is None:continue
        values=item if isinstance(item,list) else [item]
        cleaned=[str(v)[:300] for v in values if not _matches_any(str(v),private_patterns)]
        if cleaned:safe[key]=cleaned if isinstance(item,list) else cleaned[0]
    return safe

def _customer_safe_text(text:str,private_patterns:list[str])->str:
    """Remove complete lines containing internal review data before prompting/citing."""
    return "\n".join(line for line in text.splitlines() if not _matches_any(line,private_patterns)).strip()
class Pipeline:
    def __init__(self,config:ProjectConfig):
        self.config=config;self.embedder=make_embedder(config.embedding)
        store_path=os.path.expandvars(config.store.path)
        if not Path(store_path).is_absolute():store_path=str(Path(os.getenv("RAG_DATA_DIR","data"))/Path(store_path).name)
        self.store=(ChromaStore(store_path,config.collection,self.embedder.model_name) if config.store.provider=="chroma" else QdrantStore(config.store.url,config.collection,self.embedder.model_name))
        self.chunker=make_chunker(config.chunking);self.llm=make_llm(config.llm)
        self.retriever=HybridRetriever(self.store,self.embedder,config.retrieval.candidate_k,config.retrieval.rrf_k,config.retrieval.reranker,config.retrieval.reranker_model,config.retrieval.min_similarity)
        self.memory:dict[str,list[tuple[str,str]]]={};self._memory_seen:dict[str,float]={}
        manifest_root=Path(os.getenv("RAG_DATA_DIR","data"))
        collection_key=re.sub(r"[^A-Za-z0-9_-]","_",config.collection)
        self.manifest_path=manifest_root/f"{config.name}-{collection_key}-manifest.json"
        self.manifest_path.parent.mkdir(parents=True,exist_ok=True)
        try:
            self.manifest=json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except (FileNotFoundError,json.JSONDecodeError):
            # Migrate hashes for sources that are already present in this
            # model-validated collection. Empty/new collections never inherit
            # the project-wide legacy manifest, preventing false "unchanged"
            # results after an embedding-model or collection change.
            self.manifest={}
            legacy_path=manifest_root/f"{config.name}-manifest.json"
            try:legacy=json.loads(legacy_path.read_text(encoding="utf-8"))
            except (FileNotFoundError,json.JSONDecodeError):legacy={}
            indexed_ids={item["id"] for item in self.store.list_sources()}
            if indexed_ids and isinstance(legacy,dict):
                self.manifest={key:value for key,value in legacy.items() if key in indexed_ids}
                if self.manifest:
                    self.manifest_path.write_text(json.dumps(self.manifest,indent=2),encoding="utf-8")
    def ingest(self,source:str)->dict:
        self._check_source_allowed(source)
        if source.startswith(("sqlite:","postgresql:","mysql:","mssql:")):
            if not self.config.loaders.sql_query:raise ValueError("Database source requires loaders.sql_query in the project YAML")
            from loaders.database import SQLLoader
            docs=SQLLoader(self.config.loaders.sql_query).load(source)
        else:docs=load_source(source,ocr=self.config.loaders.ocr)
        return self.ingest_documents(source,docs)
    def _check_source_allowed(self, source: str) -> None:
        allowed = self.config.loaders.allowed_sources
        if not allowed:
            return
        from urllib.parse import urlparse
        name = Path(urlparse(source).path.replace("\\", "/")).name.casefold()
        if name not in {item.casefold() for item in allowed}:
            raise ValueError("This source is not allowlisted for the customer knowledge base")
    def ingest_documents(self,source:str,docs:list[Document])->dict:
        self._check_source_allowed(source)
        chunks=[]
        if not docs:return {"source":source,"chunks":0,"status":"empty"}
        if self.config.agent.name and self.config.loaders.allowed_sources:
            from urllib.parse import urlparse
            display_name=Path(urlparse(source).path.replace("\\", "/")).name
            source_id=hashlib.sha256(f"{self.config.name}:{display_name.casefold()}".encode("utf-8")).hexdigest()
            docs=[doc.model_copy(update={
                "id":f"{source_id}:p{doc.metadata['page']}" if doc.metadata.get("page") else f"{source_id}:d{index}",
                "metadata":{**doc.metadata,"source":display_name,"source_id":source_id}
            }) for index,doc in enumerate(docs)]
        digest=hashlib.sha256("\n".join(d.text for d in docs).encode("utf-8")).hexdigest()
        source_id=docs[0].metadata.get("source_id",docs[0].id)
        if self.manifest.get(source_id)==digest:return {"source":source,"source_id":source_id,"chunks":0,"status":"unchanged"}
        if self.config.chunking.strategy=="row_group":
            group=self.config.chunking.row_group_size
            for start in range(0,len(docs),group):
                batch=docs[start:start+group]
                merged=Document(id=f"{source_id}:rows{start+1}-{start+len(batch)}",text="\n".join(d.text for d in batch),metadata={**batch[0].metadata,"row_start":start+1,"row_end":start+len(batch)})
                chunks.extend(self.chunker.chunk(merged))
        else:
            for doc in docs:chunks.extend(self.chunker.chunk(doc))
        if not chunks:return {"source":source,"chunks":0,"status":"empty"}
        # Embed first so a model outage never deletes the previously indexed version.
        vectors=self.embedder.embed([d.text for d in chunks])
        self.store.delete_source(source_id)
        self.store.upsert(chunks,vectors)
        self.manifest[source_id]=digest;self.manifest_path.write_text(json.dumps(self.manifest,indent=2),encoding="utf-8")
        log.info("Ingested %s: %d documents -> %d chunks",source,len(docs),len(chunks))
        return {"source":source,"source_id":source_id,"chunks":len(chunks),"status":"ingested"}
    def ingest_path(self,path:str)->list[dict]:
        p=Path(path);items=[p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and not any(part.startswith(".") for part in x.parts))
        results=[]
        for item in items:
            try:results.append(self.ingest(str(item)))
            except Exception as exc:log.exception("Failed to ingest %s",item);results.append({"source":str(item),"status":"error","error":str(exc)})
        active={r.get("source_id") for r in results if r.get("source_id")}
        if p.is_dir():
            for old in self.store.list_sources():
                if old["id"] not in active and not Path(old["source"]).exists():
                    self.store.delete_source(old["id"]);self.manifest.pop(old["id"],None)
            self.manifest_path.write_text(json.dumps(self.manifest,indent=2),encoding="utf-8")
        return results
    def delete_document(self,document_id:str)->None:
        self.store.delete_source(document_id);self.manifest.pop(document_id,None)
        self.manifest_path.write_text(json.dumps(self.manifest,indent=2),encoding="utf-8")
    def sources(self)->list[dict]:return self.store.list_sources()
    def _memory_key(self,session_id:str)->str:
        return hashlib.sha256(f"{self.config.name}:{session_id}".encode("utf-8")).hexdigest()
    def _history(self,session_id:str|None)->list[tuple[str,str]]:
        if not session_id:return []
        key=self._memory_key(session_id);now=time.monotonic()
        seen=getattr(self,"_memory_seen",{})
        if now-seen.get(key,now)>1800:
            self.memory.pop(key,None);seen.pop(key,None)
            return []
        if key in self.memory:seen[key]=now
        return self.memory.get(key,[])
    def remember_turn(self,session_id:str|None,question:str,answer:str)->None:
        """Keep a short, expiring, bounded conversation window in process memory."""
        if not session_id:return
        key=self._memory_key(session_id);now=time.monotonic()
        seen=getattr(self,"_memory_seen",None)
        if seen is None:self._memory_seen=seen={}
        for expired in [k for k,t in seen.items() if now-t>1800]:
            seen.pop(expired,None);self.memory.pop(expired,None)
        if key not in self.memory and len(self.memory)>=10000:
            oldest=min(seen,key=seen.get) if seen else next(iter(self.memory))
            seen.pop(oldest,None);self.memory.pop(oldest,None)
        turns=self.memory.setdefault(key,[]);turns.append((question,answer));del turns[:-20];seen[key]=now
    def _rewrite(self,question:str,session_id:str|None)->str:
        history=self._history(session_id)
        if not history:return question
        recent="\n".join(f"User: {q}\nAssistant: {a}" for q,a in history[-4:])
        try:return self.llm.generate(f"Rewrite the latest question as a standalone search query using the conversation only where useful. Return only the rewritten query.\nConversation:\n{recent}\nLatest question: {question}")
        except Exception:log.exception("Query rewrite failed");return question
    def _generate_customer_answer(self,prompt:str)->str:
        system=self.config.agent.system_instructions
        method=getattr(self.llm,"generate_with_system",None)
        if callable(method):return method(system,prompt)
        combined=f"{system.strip()}\n\n{prompt}" if system.strip() else prompt
        return self.llm.generate(combined)
    def _stream_customer_answer(self,prompt:str):
        system=self.config.agent.system_instructions
        method=getattr(self.llm,"stream_with_system",None)
        if callable(method):yield from method(system,prompt)
        else:
            combined=f"{system.strip()}\n\n{prompt}" if system.strip() else prompt
            yield from self.llm.stream(combined)
    def prepare_query(self,question:str,session_id:str|None=None,top_k:int|None=None,where:dict|None=None,customer_context:dict|None=None):
        rewritten=self._rewrite(question,session_id)
        context_values=_safe_context(customer_context or {},self.config.agent.customer_context_fields,self.config.agent.private_content_patterns+self.config.agent.sensitive_context_patterns)
        retrieval_context=" ".join(f"{key.replace('_',' ')} {value if isinstance(value,str) else ' '.join(map(str,value))}" for key,value in context_values.items() if key in self.config.agent.retrieval_context_fields)
        retrieval_query=f"{rewritten} {retrieval_context}".strip()
        hits=self.retriever.retrieve(retrieval_query,top_k or self.config.retrieval.top_k,where)
        safe_hits=[]
        for hit in hits:
            clean=_customer_safe_text(hit["text"],self.config.agent.private_content_patterns+self.config.agent.sensitive_context_patterns)
            if clean:safe_hits.append((hit,clean))
        context="\n\n".join(f"[source={h['metadata'].get('source','unknown')} page={h['metadata'].get('page','n/a')} chunk_id={h['id']}]\n{text}" for h,text in safe_hits)
        safe_context=context_values
        prompt=self.config.prompt_template.format(context=context or "(no approved customer-safe context)",question=rewritten,customer_context=json.dumps(safe_context,ensure_ascii=False))
        citations=[Citation(chunk_id=h["id"],source=h["metadata"].get("source","unknown"),page=h["metadata"].get("page"),text=text[:500],score=h.get("rrf_score")) for h,text in safe_hits]
        return prompt,rewritten,citations
    def query(self,question:str,session_id:str|None=None,top_k:int|None=None,where:dict|None=None,customer_context:dict|None=None)->QueryResponse:
        guarded=self.guard_question(question,customer_context)
        if guarded:
            return QueryResponse(answer=guarded,citations=[],rewritten_query="")
        prompt,rewritten,citations=self.prepare_query(question,session_id,top_k,where,customer_context)
        if not citations:
            fallback=self.config.agent.fallback_response if self.config.agent.role else "I couldn't find this in the provided data."
            self.remember_turn(session_id,question,fallback)
            return QueryResponse(answer=fallback,citations=[],rewritten_query=rewritten)
        answer=self._generate_customer_answer(prompt)
        if self.config.agent.role and _matches_any(answer,self.config.agent.private_output_patterns):
            answer=self.config.agent.fallback_response;citations=[]
        self.remember_turn(session_id,question,answer)
        return QueryResponse(answer=answer,citations=citations,rewritten_query=rewritten)

    def guard_question(self,question:str,customer_context:dict|None=None)->str|None:
        """Apply profile-defined short-circuit safety rules before retrieval or LLM calls."""
        policy=self.config.agent
        if not policy.name:return None
        if _matches_any(question,policy.bypass_question_patterns):return policy.bypass_response
        if _matches_any(question,policy.sensitive_input_patterns):return policy.sensitive_input_response
        if _matches_any(question,policy.blocked_question_patterns):return policy.fallback_response
        if _matches_any(question,policy.out_of_scope_patterns):return policy.out_of_scope_response
        context=customer_context or {}
        for rule in policy.context_requirements:
            if _matches_any(question,rule.patterns):
                for field in rule.required_fields:
                    if context.get(field) in (None, "", [], {}):
                        return rule.missing_responses.get(field,policy.fallback_response)
        if _matches_any(question,policy.context_sensitive_patterns):
            for field in policy.context_required_fields:
                if context.get(field) in (None, "", [], {}):
                    return policy.context_questions.get(field,policy.fallback_response)
        if not (customer_context or {}).get("current_onboarding_step") and _matches_any(question,policy.clarification_patterns):return policy.clarification_response
        return None

    def safe_stream_answer(self,prompt:str,citations:list[Citation],question:str="",customer_context:dict|None=None)->str:
        """Buffer and screen generated text before exposing any customer-facing tokens."""
        guarded=self.guard_question(question,customer_context)
        if guarded:return guarded
        if not citations:return self.config.agent.fallback_response if self.config.agent.role else "I couldn't find this in the provided data."
        answer="".join(self._stream_customer_answer(prompt))
        return self.config.agent.fallback_response if self.config.agent.role and _matches_any(answer,self.config.agent.private_output_patterns) else answer
