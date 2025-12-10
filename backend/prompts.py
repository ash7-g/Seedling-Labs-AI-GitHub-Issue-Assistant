LLM_PROMPT = """
You are an AI assistant. You MUST return ONLY valid JSON.
No explanations, no markdown, no text before or after the JSON.

Return JSON with this exact structure:

{{
  "summary": "A one-sentence summary.",
  "type": "bug | feature_request | documentation | question | other",
  "priority_score": "A number 1-5 with justification.",
  "suggested_labels": ["label1", "label2"],
  "potential_impact": "A brief sentence about user impact."
}}

IMPORTANT:
- Output only JSON.
- Do not wrap JSON in backticks or markdown.

Issue Title:
{title}

Issue Body:
{body}

Issue Comments:
{comments}
"""
