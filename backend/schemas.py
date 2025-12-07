from pydantic import BaseModel
from typing import List, Union

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

class IssueAnalysis(BaseModel):
    summary: str
    type: str
    priority_score: Union[str, int]   # <-- FIXED (accepts both)
    suggested_labels: List[str]
    potential_impact: str

