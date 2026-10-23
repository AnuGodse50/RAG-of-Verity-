"""HTTP and HTML URL loader."""
import hashlib
import tempfile
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
from core.models import Document
from core.interfaces import Loader
from loaders.registry import register_loader
@register_loader("__url__")
class URLLoader(Loader):
    def load(self, source: str) -> list[Document]:
        response=httpx.get(source,timeout=30,follow_redirects=True); response.raise_for_status()
        content_type=response.headers.get("content-type","").split(";",1)[0].lower()
        mime_ext={"application/pdf":".pdf","text/plain":".txt","text/markdown":".md","text/csv":".csv","application/json":".json","application/vnd.openxmlformats-officedocument.wordprocessingml.document":".docx"}.get(content_type)
        suffix=Path(source.split("?",1)[0]).suffix.lower() or mime_ext
        if content_type!="text/html" and content_type!="application/xhtml+xml" and suffix in {".pdf",".txt",".md",".csv",".json",".docx",".xlsx"}:
            from loaders.registry import load_source
            with tempfile.NamedTemporaryFile(suffix=suffix,delete=True) as tmp:
                tmp.write(response.content);tmp.flush();docs=load_source(tmp.name)
            sid=hashlib.sha256(source.encode()).hexdigest()
            for doc in docs:doc.metadata.update({"source":source,"source_id":sid,"type":suffix.lstrip(".")})
            return docs
        soup=BeautifulSoup(response.text,"html.parser")
        for tag in soup(["script","style","nav","footer"]): tag.decompose()
        text=soup.get_text("\n",strip=True); sid=hashlib.sha256(source.encode()).hexdigest()
        return [Document(id=sid,text=text,metadata={"source":source,"source_id":sid,"type":"url","title":soup.title.string if soup.title else source})]
