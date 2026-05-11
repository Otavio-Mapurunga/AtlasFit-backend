from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import auth

app = FastAPI(
    title="AtlasFit API",
    description="API de autenticação e gerenciamento de treinos do AtlasFit",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS — permite o front-end Next.js se comunicar com a API em desenvolvimento
# ---------------------------------------------------------------------------
origins = [
    "http://localhost:3000",   # Next.js dev server
    "http://127.0.0.1:3000",
    # Adicione aqui o domínio de produção quando fizer o deploy
    # "https://seu-dominio.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(auth.router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "AtlasFit API está rodando 🚀"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
