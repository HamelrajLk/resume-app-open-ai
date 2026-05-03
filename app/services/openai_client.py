import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment.")

client = OpenAI(api_key=_api_key)
