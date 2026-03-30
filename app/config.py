import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=api_key)