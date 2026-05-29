from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.ia_router import router as ia_router
from app.routes.treino_router import router as treino_router
from app.routes.execucao_router import router as execucao_router
from app.auth.routes import router as auth_router

app = FastAPI()

app.include_router(ia_router)
app.include_router(treino_router)
app.include_router(execucao_router)
app.include_router(auth_router)

# config cors pro next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://v0-projeto-atlas-fit.vercel.app","http://26.186.121.188:3000"], 
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def red_road():
    return {"mensagem": "API funcionando"}
