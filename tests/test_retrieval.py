from retrievers.hybrid import HybridRetriever
class FakeEmbedder:
    def embed(self,texts):return [[1.0,0.0] for _ in texts]
class FakeStore:
    def dense_search(self,vector,limit,where=None):return [{"id":"a","text":"apple orchard","metadata":{"source":"a.txt"},"score":.9}]
    def all_documents(self):return [{"id":"a","text":"apple orchard","metadata":{"source":"a.txt"}},{"id":"b","text":"banana grove","metadata":{"source":"b.txt"}}]
def test_hybrid_finds_dense_and_keyword_results():
    result=HybridRetriever(FakeStore(),FakeEmbedder()).retrieve("banana",2)
    assert {r["id"] for r in result}=={"a","b"}
    assert result[0]["rrf_score"]>0
