from pydantic import BaseModel

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

class IssueAnalysis(BaseModel):
    summary: str
    type: str
    priority_score: str
    suggested_labels: list[str]
    potential_impact: str
