import os
import secrets
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client,Client

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API=os.getenv("GROQ_API_KEY")
SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_KEY=os.getenv("SUPABASE_KEY")
VITE_NEON_DATA_API=os.getenv("VITE_NEON_DATA_API")
VITE_NEON_AUTH_URL=os.getenv("VITE_NEON_AUTH_URL")


# JWT secret: use provided env or generate a secure default (>=32 bytes)
_jwt_env = os.getenv("JWT_SECRET")
if _jwt_env and len(_jwt_env) >= 32:
    JWT_SECRET = _jwt_env
else:
    # generate a secure random secret when not provided or too short
    JWT_SECRET = secrets.token_urlsafe(48)
    print("[WARN] JWT_SECRET ausente ou inseguro — gerando segredo temporário para desenvolvimento.")

JWT_ALGORITHM="HS256"
JWT_EXPIRES_MINUTES=int(os.getenv("JWT_EXPIRES_MINUTES", "1440"))
supabase: Client=create_client(SUPABASE_URL,SUPABASE_KEY)

if not GROQ_API:
    raise ValueError("GROQ_API_KEY não encontrada no .env")

groq_client= Groq(api_key=GROQ_API)
