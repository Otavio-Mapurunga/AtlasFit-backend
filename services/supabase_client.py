import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Garante que o .env seja carregado da pasta backend/, independente de onde
# o uvicorn for iniciado
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise EnvironmentError(
        "As variáveis SUPABASE_URL e SUPABASE_KEY são obrigatórias. "
        "Verifique seu arquivo .env"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
