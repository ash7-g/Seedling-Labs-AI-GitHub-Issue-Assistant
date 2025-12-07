import requests
import json
from openai import OpenAI

from backend.prompts import LLM_PROMPT
from backend.schemas import IssueAnalysis
from backend.config import OPENAI_API_KEY, OPENAI_MODEL, GITHUB_TOKEN

client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_issue(repo_url: str, issue_number: int):
    owner_repo = repo_url.replace("https://github.com/", "")
    api = f"https://api.github.com/repos/{owner_repo}"

    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    issue = requests.get(f"{api}/issues/{issue_number}", headers=headers).json()
    comments = requests.get(f"{api}/issues/{issue_number}/comments", headers=headers).json()

    title = issue.get("title", "")
    body = issue.get("body", "")
    comment_text = "\n---\n".join(c.get("body", "") for c in comments) or "No comments."

    return title, body, comment_text


def analyze_issue(repo_url: str, issue_number: int) -> IssueAnalysis:
    title, body, comments = fetch_issue(repo_url, issue_number)

    prompt = LLM_PROMPT.format(
        title=title or "",
        body=body or "",
        comments=comments or "",
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    # FIXED: new OpenAI SDK uses .content instead of ["content"]
    raw = response.choices[0].message.content

    # Parse JSON response strictly
    data = json.loads(raw)

    return IssueAnalysis(**data)
