"""PDF loader with optional OCR fallback for scanned pages."""
from pathlib import Path
import hashlib
from core.models import Document
from core.interfaces import Loader
from loaders.registry import register_loader
@register_loader(".pdf")
class PDFLoader(Loader):
    def load(self, source: str) -> list[Document]:
        from pypdf import PdfReader
        path = Path(source); sid = hashlib.sha256(str(path.resolve()).encode()).hexdigest()
        result = []
        for page_no, page in enumerate(PdfReader(str(path)).pages, 1):
            content = (page.extract_text() or "").strip(); used_ocr = False
            if not content:
                try:
                    import pytesseract
                    from pdf2image import convert_from_path
                    import os
                    if os.getenv("TESSERACT_CMD"): pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]
                    content = pytesseract.image_to_string(convert_from_path(str(path), first_page=page_no, last_page=page_no)[0]).strip()
                    used_ocr = bool(content)
                except ImportError:
                    content = ""
            result.append(Document(id=f"{sid}:p{page_no}", text=content, metadata={"source": str(path), "source_id": sid, "page": page_no, "type": "pdf", "ocr": used_ocr}))
        return result
