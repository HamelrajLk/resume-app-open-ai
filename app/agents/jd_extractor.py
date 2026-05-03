import json
from app.prompts import EXTRACT_JD_DETAILS
from app.services.openai_client import client


def analyze_jd(jd_text: str) -> dict:
    prompt = EXTRACT_JD_DETAILS.format(jd_text=jd_text)
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
        raise ValueError(f"JD extractor returned invalid JSON: {e}\nRaw response: {raw}")
