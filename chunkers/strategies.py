"""Dataset-neutral chunking strategies."""
import re
from core.interfaces import Chunker
from core.models import Document
from core.config import ChunkingConfig

class RecursiveChunker(Chunker):
    def __init__(self,size:int,overlap:int): self.size=size; self.overlap=overlap
    def chunk(self,document:Document)->list[Document]:
        text=document.text.strip()
        if not text:return []
        if len(text)<=self.size: pieces=[text]
        else:
            pieces=[]; start=0
            while start<len(text):
                end=min(start+self.size,len(text))
                if end<len(text):
                    cut=max((text.rfind(sep,start,end) for sep in ("\n\n","\n",". "," ")),default=-1)
                    if cut>start+self.size//2:end=cut+1
                piece=text[start:end].strip()
                if piece:pieces.append(piece)
                if end>=len(text):break
                start=max(start+1,end-self.overlap)
        return [Document(id=f"{document.id}:c{i}",text=part,metadata={**document.metadata,"chunk_id":f"{document.id}:c{i}"}) for i,part in enumerate(pieces)]

class StructureChunker(RecursiveChunker):
    def chunk(self,document:Document)->list[Document]:
        # Keep heading sections together whenever they fit the configured size.
        sections=re.split(r"(?m)(?=^#{1,6}\s+)",document.text)
        out=[]
        for section in sections:
            if section.strip(): out.extend(super().chunk(document.model_copy(update={"text":section.strip(),"id":f"{document.id}:s{len(out)}"})))
        return out

class CodeChunker(RecursiveChunker):
    def chunk(self,document:Document)->list[Document]:
        boundaries=list(re.finditer(r"(?m)^(?:\s*(?:async\s+)?def\s+|\s*class\s+|\s*(?:export\s+)?(?:async\s+)?function\s+)",document.text))
        if len(boundaries)<2:return super().chunk(document)
        pieces=[]
        for i,m in enumerate(boundaries):
            a=m.start(); b=boundaries[i+1].start() if i+1<len(boundaries) else len(document.text)
            unit=document.text[a:b].strip()
            if len(unit)>self.size: pieces.extend(super().chunk(document.model_copy(update={"text":unit,"id":f"{document.id}:fn{i}"})))
            elif unit: pieces.append(unit)
        return [Document(id=f"{document.id}:c{i}",text=t,metadata={**document.metadata,"chunk_id":f"{document.id}:c{i}"}) for i,t in enumerate(pieces)]

class RowGroupChunker(RecursiveChunker):
    def __init__(self,size:int,overlap:int,row_group_size:int):super().__init__(size,overlap);self.rows=row_group_size
    def chunk(self,document:Document)->list[Document]:
        # Loaders provide one document per record. Group compatible records in the ingest orchestrator.
        return super().chunk(document)

def make_chunker(config:ChunkingConfig)->Chunker:
    cls={"recursive":RecursiveChunker,"structure":StructureChunker,"code":CodeChunker,"row_group":lambda s,o:RowGroupChunker(s,o,config.row_group_size)}[config.strategy]
    return cls(config.chunk_size,config.overlap)
