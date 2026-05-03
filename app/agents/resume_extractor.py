import json
from app.prompts import EXTRACT_CANDIDATE_DETAILS
from app.services.openai_client import client


def generate_response(resume_data: str) -> dict:
    prompt = EXTRACT_CANDIDATE_DETAILS.format(resume_text=resume_data)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
        raw = raw.rsplit("```", 1)[0].strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Resume extractor returned invalid JSON: {e}\nRaw response: {raw}")
