import requests
import json
from openai import OpenAI

from backend.prompts import LLM_PROMPT
from backend.schemas import IssueAnalysis
from backend.config import OPENAI_API_KEY, OPENAI_MODEL, GITHUB_TOKEN

client = OpenAI(api_key=OPENAI_API_KEY)


def _safe_github_get(url: str, headers: dict):
    """Safely call GitHub API and ensure JSON response"""
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        raise RuntimeError(
            f"GitHub API error {resp.status_code}: {resp.text[:200]}"
        )

    content_type = resp.headers.get("Content-Type", "")
    if "application/json" not in content_type:
        raise RuntimeError(
            "GitHub returned non-JSON response. "
            "Check GITHUB_TOKEN or rate limits."
        )

    return resp.json()


def fetch_issue(repo_url: str, issue_number: int):
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Invalid GitHub repository URL")

    owner_repo = repo_url.replace("https://github.com/", "").strip("/")
    api_base = f"https://api.github.com/repos/{owner_repo}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    issue = _safe_github_get(
        f"{api_base}/issues/{issue_number}", headers
    )

    comments = _safe_github_get(
        f"{api_base}/issues/{issue_number}/comments", headers
    )

    title = issue.get("title", "")
    body = issue.get("body", "")
    comment_text = (
        "\n---\n".join(c.get("body", "") for c in comments)
        if comments else "No comments."
    )

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
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise RuntimeError(
            "LLM response was not valid JSON. "
            "Adjust prompt or model."
        )

    return IssueAnalysis(**data)
