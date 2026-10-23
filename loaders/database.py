"""Read-only SQL database loader (SQLAlchemy URL, explicit SELECT only)."""
import hashlib
from sqlalchemy import create_engine, text as sql_text
from core.models import Document
from core.interfaces import Loader
class SQLLoader(Loader):
    def __init__(self, query: str):
        if not query.lstrip().lower().startswith(("select", "with")): raise ValueError("SQL loader only accepts read-only SELECT/WITH queries")
        self.query=query
    def load(self, source: str) -> list[Document]:
        engine=create_engine(source); sid=hashlib.sha256((source+self.query).encode()).hexdigest()
        with engine.connect() as conn: rows=conn.execute(sql_text(self.query)).mappings().all()
        return [Document(id=f"{sid}:row{i}",text=str(dict(row)),metadata={"source":source,"source_id":sid,"type":"sql","row":i}) for i,row in enumerate(rows)]
