from fastapi import APIRouter
from app.services.gemini_service import gerar_treino

router = APIRouter()

@router.get("/ai-test")
def testar_ai():

    resposta = gerar_treino("diga apenas: api funcionando")

    return {"resposta": resposta}