from core.config import ChunkingConfig
from core.models import Document
from chunkers import make_chunker
def test_recursive_chunk_size_and_overlap():
    doc=Document(id="x",text="alpha beta gamma delta "*12,metadata={"source":"x"})
    chunks=make_chunker(ChunkingConfig(chunk_size=120,overlap=8)).chunk(doc)
    assert len(chunks)>1
    assert all(len(c.text)<=120 for c in chunks)
    assert all(c.metadata["source"]=="x" for c in chunks)
def test_structure_chunker_keeps_section_headings():
    doc=Document(id="x",text="# One\nfirst\n# Two\nsecond")
    chunks=make_chunker(ChunkingConfig(strategy="structure",chunk_size=100,overlap=0)).chunk(doc)
    assert any("# One" in c.text for c in chunks)
    assert any("# Two" in c.text for c in chunks)
