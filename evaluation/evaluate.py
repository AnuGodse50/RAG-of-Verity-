"""Evaluate retrieval using JSON or CSV question/expected-source pairs."""
import csv, json
from pathlib import Path
from core.pipeline import Pipeline
def load_cases(path:str)->list[dict]:
    p=Path(path)
    if p.suffix.lower()==".csv":
        with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
    data=json.loads(p.read_text(encoding="utf-8"));return data if isinstance(data,list) else data.get("cases",[])
def evaluate(pipeline:Pipeline,cases:list[dict],k:int|None=None)->dict:
    hits=0;rr=0
    for case in cases:
        expected=case.get("expected_sources",case.get("expected_source",[]))
        expected={expected} if isinstance(expected,str) else set(expected)
        results=pipeline.retriever.retrieve(case["question"],k or pipeline.config.retrieval.top_k)
        rank=next((i for i,r in enumerate(results,1) if r["metadata"].get("source") in expected or r["metadata"].get("source_id") in expected),None)
        hits+=rank is not None;rr+=1/rank if rank else 0
    n=max(1,len(cases));return {"questions":len(cases),"hit_rate_at_k":hits/n,"mrr":rr/n,"k":k or pipeline.config.retrieval.top_k}
