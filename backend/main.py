from fastapi import FastAPI
from backend.schemas import IssueRequest, IssueAnalysis
from backend.analyzer import analyze_issue
from fastapi.middleware.cors import CORSMiddleware

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
