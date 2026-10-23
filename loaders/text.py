"""Text and source-code loaders."""
from pathlib import Path
from core.models import Document
from core.interfaces import Loader
from loaders.registry import register_loader
@register_loader(".txt", ".md", ".markdown", ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".c", ".cpp", ".h", ".html", ".htm")
class TextLoader(Loader):
    def load(self, source: str) -> list[Document]:
        path = Path(source)
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix.lower() in {".html", ".htm"}:
            from bs4 import BeautifulSoup
            text = BeautifulSoup(text, "html.parser").get_text("\n", strip=True)
        import hashlib
        source_id = hashlib.sha256(str(path.resolve()).encode()).hexdigest()
        return [Document(id=source_id, text=text, metadata={"source": str(path), "source_id": source_id, "type": path.suffix.lower().lstrip("."), "timestamp": path.stat().st_mtime})]
