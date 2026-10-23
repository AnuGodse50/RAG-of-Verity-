"""Command line entry point: python -m evaluation <project> <cases.json|csv>."""
import argparse,json
from core.config import load_project_config
from core.pipeline import Pipeline
from evaluation.evaluate import evaluate,load_cases
def main():
    parser=argparse.ArgumentParser();parser.add_argument("project");parser.add_argument("cases");parser.add_argument("--k",type=int);args=parser.parse_args()
    print(json.dumps(evaluate(Pipeline(load_project_config(args.project)),load_cases(args.cases),args.k),indent=2))
if __name__=="__main__":main()
