from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.analyzer import analyze_issue
from backend.schemas import IssueRequest, IssueAnalysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze", response_model=IssueAnalysis)
def analyze(request: IssueRequest):
    return analyze_issue(request.repo_url, request.issue_number)
