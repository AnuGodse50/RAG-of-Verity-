"""Dense plus BM25 retrieval fused with reciprocal rank fusion."""
from rank_bm25 import BM25Okapi
from core.interfaces import Embedder, VectorStore
class HybridRetriever:
    def __init__(self,store:VectorStore,embedder:Embedder,candidate_k:int=30,rrf_k:int=60,reranker:bool=False,reranker_model:str="BAAI/bge-reranker-v2-m3",min_similarity:float=-1.0):
        self.store=store;self.embedder=embedder;self.k=candidate_k;self.rrf_k=rrf_k;self.reranker=reranker;self.reranker_model=reranker_model;self.min_similarity=min_similarity;self._ranker=None
    def retrieve(self,query:str,top_k:int,where:dict|None=None)->list[dict]:
        dense=self.store.dense_search(self.embedder.embed([query])[0],self.k,where)
        docs=self.store.all_documents() if hasattr(self.store,"all_documents") else []
        if where:docs=[d for d in docs if all(d["metadata"].get(k)==v for k,v in where.items())]
        tokenized=[d["text"].lower().split() for d in docs]
        lexical=[]
        if docs and any(tokenized):
            scores=BM25Okapi(tokenized).get_scores(query.lower().split())
            lexical=[docs[i] | {"score":float(scores[i])} for i in sorted(range(len(scores)),key=lambda j:scores[j],reverse=True)[:self.k]]
        fused={}
        for ranking in (dense,lexical):
            for rank,item in enumerate(ranking,1):
                key=item["id"];fused.setdefault(key,item);fused[key]["rrf_score"]=fused[key].get("rrf_score",0)+1/(self.rrf_k+rank)
        result=sorted(fused.values(),key=lambda x:x["rrf_score"],reverse=True)
        # Only dense candidates carry a comparable cosine similarity. Require
        # one sufficiently close match before the generator sees any context.
        result=[item for item in result if item.get("score",-1.0)>=self.min_similarity]
        if self.reranker and result:
            if self._ranker is None:
                from sentence_transformers import CrossEncoder
                self._ranker=CrossEncoder(self.reranker_model)
            pairs=[(query,d["text"]) for d in result[:50]]
            scores=self._ranker.predict(pairs)
            for d,s in zip(result,scores):d["rerank_score"]=float(s)
            result.sort(key=lambda x:x.get("rerank_score",0),reverse=True)
        return result[:top_k]
