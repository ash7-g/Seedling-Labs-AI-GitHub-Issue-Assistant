LLM_PROMPT = """
You are an AI assistant analyzing GitHub issues.

Return ONLY a valid JSON object matching this schema:

{{
 "summary": "A one-sentence summary.",
 "type": "bug | feature_request | documentation | question | other",
 "priority_score": "A number 1-5 with justification.",
 "suggested_labels": ["2-3 labels"],
 "potential_impact": "A brief sentence about user impact."
}}

Issue Title:
{title}

Issue Body:
{body}

Issue Comments:
{comments}
"""
