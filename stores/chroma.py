"""Persistent Chroma adapter with model consistency enforcement."""
import json, os, re
from pathlib import Path
from core.interfaces import VectorStore
from core.models import Document
class ChromaStore(VectorStore):
    def __init__(self,path:str,collection:str,model_name:str):
        import chromadb
        base=Path(path);base.mkdir(parents=True,exist_ok=True)
        self.client=chromadb.PersistentClient(path=str(base));self.name=re.sub(r"[^a-zA-Z0-9_-]","_",collection)[:60].lower()
        self.col=self.client.get_or_create_collection(self.name,metadata={"embedding_model":model_name,"hnsw:space":"cosine"})
        stored=(self.col.metadata or {}).get("embedding_model")
        if stored and stored!=model_name:raise ValueError(f"Collection {self.name!r} uses embedding model {stored!r}, cannot use {model_name!r}; create a new collection or re-embed.")
        if not stored:
            if self.col.count():
                raise ValueError(f"Collection {self.name!r} has vectors but no embedding model identity; create a fresh collection before ingesting.")
            raise ValueError(f"Collection {self.name!r} has no embedding model metadata; choose a new collection name.")
    def upsert(self,documents:list[Document],vectors:list[list[float]])->None:
        if not documents:return
        metadata=[]
        for doc in documents:
            flat={k:v for k,v in doc.metadata.items() if not k.startswith("_") and isinstance(v,(str,int,float,bool))}
            metadata.append({"_metadata":json.dumps(doc.metadata,default=str),**flat})
        self.col.upsert(ids=[d.id for d in documents],embeddings=vectors,documents=[d.text for d in documents],metadatas=metadata)
    def dense_search(self,query_vector:list[float],limit:int,where:dict|None=None)->list[dict]:
        query_args={"query_embeddings":[query_vector],"n_results":limit,"include":["documents","metadatas","distances"]}
        if where:query_args["where"]=where
        result=self.col.query(**query_args)
        out=[]
        for i,id_ in enumerate(result["ids"][0]):
            raw=result["metadatas"][0][i] or {};out.append({"id":id_,"text":result["documents"][0][i],"metadata":json.loads(raw.get("_metadata","{}")),"score":1-float(result["distances"][0][i])})
        return out
    def delete_source(self,source_id:str)->None:
        got=self.col.get(include=["metadatas"]);ids=[]
        for i,meta in enumerate(got["metadatas"] or []):
            data=json.loads((meta or {}).get("_metadata","{}"))
            if data.get("source_id")==source_id:ids.append(got["ids"][i])
        if ids:self.col.delete(ids=ids)
    def list_sources(self)->list[dict]:
        got=self.col.get(include=["metadatas"]);seen={}
        for i,meta in enumerate(got["metadatas"] or []):
            data=json.loads((meta or {}).get("_metadata","{}"));sid=data.get("source_id",data.get("source",got["ids"][i]));row=seen.setdefault(sid,{"id":sid,"source":data.get("source",sid),"type":data.get("type","unknown"),"chunks":0})
            row["chunks"]+=1
        return list(seen.values())
    def all_documents(self)->list[dict]:
        got=self.col.get(include=["documents","metadatas"]);out=[]
        for i,id_ in enumerate(got["ids"]):
            raw=got["metadatas"][i] or {};out.append({"id":id_,"text":got["documents"][i],"metadata":json.loads(raw.get("_metadata","{}"))})
        return out
