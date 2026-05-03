import json
from app.prompts import CANDIDATE_EVALUATION
from app.services.openai_client import client


def candidate_evaluation(resume_data: dict, jd_data: dict) -> dict:
    prompt = CANDIDATE_EVALUATION.format(
        resume_json=json.dumps(resume_data),
        jd_json=json.dumps(jd_data)
    )
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
        raise ValueError(f"Evaluation agent returned invalid JSON: {e}\nRaw response: {raw}")
