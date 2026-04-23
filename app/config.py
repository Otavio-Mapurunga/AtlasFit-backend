import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client,Client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv()

GROQ_API=os.getenv("GROQ_API_KEY")
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")
supabase: Client=create_client(SUPABASE_URL,SUPABASE_KEY)

if not GROQ_API:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

groq_client= Groq(api_key=GROQ_API)
