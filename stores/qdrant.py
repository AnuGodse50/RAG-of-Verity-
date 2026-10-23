"""Qdrant vector store adapter implementing the common VectorStore contract."""
import json, re, uuid
from qdrant_client import QdrantClient, models
from core.interfaces import VectorStore
from core.models import Document
class QdrantStore(VectorStore):
    def __init__(self,url:str|None,collection:str,model_name:str):
        self.client=QdrantClient(url=url) if url else QdrantClient(path="./data/qdrant")
        self.name=re.sub(r"[^a-zA-Z0-9_-]","_",collection)[:60]
        self.model_name=model_name;self._size=None
        if self.client.collection_exists(self.name):
            info=self.client.get_collection(self.name);self._size=info.config.params.vectors.size
            # Qdrant collection metadata is stored in a sentinel point to enforce model consistency.
            sentinel=self.client.retrieve(self.name,ids=[0],with_payload=True,with_vectors=False)
            saved=sentinel[0].payload.get("embedding_model") if sentinel else None
            if saved and saved!=model_name:raise ValueError(f"Collection {self.name!r} uses embedding model {saved!r}, cannot use {model_name!r}")
    def _ensure(self,size:int):
        if self._size is not None:
            if self._size!=size:raise ValueError(f"Qdrant vector dimension mismatch: collection={self._size}, model={size}")
            return
        self.client.create_collection(self.name,vectors_config=models.VectorParams(size=size,distance=models.Distance.COSINE))
        self._size=size
        self.client.upsert(self.name,points=[models.PointStruct(id=0,vector=[0.0]*size,payload={"embedding_model":self.model_name,"_sentinel":True})])
    def upsert(self,documents:list[Document],vectors:list[list[float]])->None:
        if not documents:return
        self._ensure(len(vectors[0]));points=[]
        for d,v in zip(documents,vectors):
            payload={"document_id":d.id,"text":d.text,"metadata_json":json.dumps(d.metadata,default=str),"source_id":d.metadata.get("source_id","")}
            payload.update({f"meta_{k}":v for k,v in d.metadata.items() if isinstance(v,(str,int,float,bool))})
            points.append(models.PointStruct(id=str(uuid.uuid5(uuid.NAMESPACE_URL,d.id)),vector=v,payload=payload))
        self.client.upsert(self.name,points=points)
    def dense_search(self,query_vector:list[float],limit:int,where:dict|None=None)->list[dict]:
        query_filter=None
        if where:query_filter=models.Filter(must=[models.FieldCondition(key=f"meta_{k}",match=models.MatchValue(value=v)) for k,v in where.items()])
        hits=self.client.search(self.name,query_vector=query_vector,limit=limit,query_filter=query_filter)
        return [{"id":h.payload.get("document_id",str(h.id)),"text":h.payload.get("text",""),"metadata":json.loads(h.payload.get("metadata_json","{}")),"score":h.score} for h in hits if not h.payload.get("_sentinel")]
    def delete_source(self,source_id:str)->None:
        self.client.delete(self.name,points_selector=models.FilterSelector(filter=models.Filter(must=[models.FieldCondition(key="source_id",match=models.MatchValue(value=source_id))])))
    def all_documents(self)->list[dict]:
        out=[];offset=None
        while True:
            points,offset=self.client.scroll(self.name,limit=500,offset=offset,with_payload=True,with_vectors=False)
            out.extend({"id":p.payload.get("document_id",str(p.id)),"text":p.payload.get("text",""),"metadata":json.loads(p.payload.get("metadata_json","{}"))} for p in points if not p.payload.get("_sentinel"))
            if offset is None:break
        return out
    def list_sources(self)->list[dict]:
        sources={}
        for doc in self.all_documents():
            meta=doc["metadata"];sid=meta.get("source_id",meta.get("source",doc["id"]))
            row=sources.setdefault(sid,{"id":sid,"source":meta.get("source",sid),"type":meta.get("type","unknown"),"chunks":0});row["chunks"]+=1
        return list(sources.values())
