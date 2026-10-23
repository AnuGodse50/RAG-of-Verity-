"""Extension-based loader registry."""
from pathlib import Path
from urllib.parse import urlparse
from core.models import Document
from core.interfaces import Loader
_LOADERS: dict[str, type[Loader]] = {}

def registered_extensions() -> set[str]:
    """Return normalized extensions supported by the loaded loader plugins."""
    return set(_LOADERS)

def register_loader(*extensions: str):
    def decorate(cls: type[Loader]):
        for ext in extensions: _LOADERS[ext.lower()] = cls
        return cls
    return decorate
def load_source(source: str, ocr: bool = True) -> list[Document]:
    parsed = urlparse(source)
    ext = Path(parsed.path).suffix.lower()
    if parsed.scheme in {"http", "https"}: ext = "__url__"
    if ext not in _LOADERS:
        raise ValueError(f"No loader registered for {ext or 'extensionless source'}: {source}")
    return _LOADERS[ext]().load(source)  # type: ignore[call-arg]
