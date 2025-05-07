import os
from dotenv import load_dotenv

load_dotenv()

LLM_URL = os.getenv("LLM_URL", "http://llm_app:5005")
