import json
from loaders import load_source
def test_text_loader(tmp_path):
    path=tmp_path/"note.txt";path.write_text("hello RAG",encoding="utf-8")
    docs=load_source(str(path))
    assert docs[0].text=="hello RAG" and docs[0].metadata["type"]=="txt"
def test_json_loader(tmp_path):
    path=tmp_path/"items.json";path.write_text(json.dumps([{"a":1},{"b":2}]),encoding="utf-8")
    docs=load_source(str(path))
    assert len(docs)==1 and '"a": 1' in docs[0].text
