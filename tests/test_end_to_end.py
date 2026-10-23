"""Small deterministic pipeline path through ingestion, hybrid retrieval, and citations."""
from core.models import Document
from core.pipeline import Pipeline
def test_ingest_and_citation_shape(tmp_path,monkeypatch):
    from core.config import ProjectConfig
    class Emb:
        model_name="fake-v1"
        def embed(self,texts):return [[1.,0.] for _ in texts]
    class Store:
        docs=[]
        def upsert(self,docs,vectors):self.docs=list(docs)
        def delete_source(self,sid):self.docs=[]
        def dense_search(self,vector,limit,where=None):return [{"id":d.id,"text":d.text,"metadata":d.metadata,"score":1.0} for d in self.docs[:limit]]
        def all_documents(self):return [{"id":d.id,"text":d.text,"metadata":d.metadata} for d in self.docs]
        def list_sources(self):return []
    class LLM:
        def generate(self,prompt):return "The demo says hybrid search combines dense and BM25. [sample.txt, chunk]"
    config=ProjectConfig(name="test",collection="test")
    pipe=Pipeline.__new__(Pipeline);pipe.config=config;pipe.embedder=Emb();pipe.store=Store();pipe.llm=LLM()
    from chunkers import make_chunker
    from retrievers.hybrid import HybridRetriever
    pipe.chunker=make_chunker(config.chunking);pipe.retriever=HybridRetriever(pipe.store,pipe.embedder);pipe.memory={};pipe.manifest_path=tmp_path/"m.json";pipe.manifest={}
    import core.pipeline as module
    monkeypatch.setattr(module,"load_source",lambda source, **kwargs:[Document(id="s",text="Dense and BM25 use reciprocal rank fusion.",metadata={"source":"sample.txt","source_id":"sid","type":"txt"})])
    result=pipe.ingest("sample.txt");answer=pipe.query("How is hybrid search done?")
    assert result["chunks"]==1 and answer.citations[0].source=="sample.txt"
