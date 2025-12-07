import requests
import json

from backend.prompts import LLM_PROMPT_TEMPLATE
from backend.schemas import IssueAnalysis
from backend.config import OPENAI_API_KEY, OPENAI_MODEL, GITHUB_TOKEN

from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_issue_data(repo_url: str, issue_number: int):
    """Fetch title, body, and comments from GitHub."""
    owner_repo = repo_url.replace("https://github.com/", "").strip("/")
    api_base = f"https://api.github.com/repos/{owner_repo}"

    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    # Fetch issue
    issue_res = requests.get(f"{api_base}/issues/{issue_number}", headers=headers)

    if issue_res.status_code != 200:
        raise ValueError(f"GitHub API error {issue_res.status_code}: {issue_res.text}")

    issue = issue_res.json()

    # Fetch comments
    comments_res = requests.get(f"{api_base}/issues/{issue_number}/comments", headers=headers)
    comments = comments_res.json() if comments_res.status_code == 200 else []

    comment_bodies = "\n---\n".join(
        [c.get("body", "") for c in comments]
    ) if comments else "No comments."

    title = issue.get("title", "No title")
    body = issue.get("body", "No body")

    return title, body, comment_bodies


def analyze_issue(repo_url: str, issue_number: int) -> IssueAnalysis:
    """Format prompt, call LLM, parse JSON, return IssueAnalysis."""
    title, body, comments = fetch_issue_data(repo_url, issue_number)

    prompt = LLM_PROMPT_TEMPLATE.format(
        title=title,
        body=body,
        comments=comments
    )

    response = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    raw_output = response.choices[0].message.content


    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}\nRaw: {raw_output}")

    return IssueAnalysis(**parsed)
