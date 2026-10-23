"""rag ingest and rag ask commands."""
import argparse, json, logging
from dotenv import load_dotenv
from core.config import load_project_config
from core.pipeline import Pipeline
def main():
    load_dotenv()
    parser=argparse.ArgumentParser(prog="rag");sub=parser.add_subparsers(dest="command",required=True)
    ing=sub.add_parser("ingest");ing.add_argument("project");ing.add_argument("path")
    ask=sub.add_parser("ask");ask.add_argument("project");ask.add_argument("question");ask.add_argument("--session")
    src=sub.add_parser("sources");src.add_argument("project")
    args=parser.parse_args();logging.basicConfig(level=logging.INFO)
    rag=Pipeline(load_project_config(args.project))
    if args.command=="ingest":print(json.dumps(rag.ingest_path(args.path),indent=2,ensure_ascii=False))
    elif args.command=="ask":print(rag.query(args.question,args.session).model_dump_json(indent=2))
    else:print(json.dumps(rag.sources(),indent=2))
if __name__=="__main__":main()
