from openai import OpenAI
import os
from dotenv import load_dotenv

from app.prompts import EXTRACT_CANDIDATE_DETAILS

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(resume_data: str) -> str:
    prompt = EXTRACT_CANDIDATE_DETAILS.format(resume_text=resume_data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content