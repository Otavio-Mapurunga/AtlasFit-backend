from fastapi import APIRouter, Depends, HTTPException
from app.services.groq_service import GroqServiceError, GroqTemporaryUnavailableError, gerar_treino
from app.services import workout_service
from app.schemas.treino_schemas import TreinoResponse
from app.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/ia")

@router.get("/test")
def testar_ai():
    try:
        resposta = gerar_treino("diga apenas: api funcionando")
    except GroqTemporaryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except GroqServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return {"resposta": resposta}


@router.post("/generate-workout", response_model=TreinoResponse)
def treino_gerado(user_id: str = Depends(get_current_user_id)):
    """Gera e salva um novo treino a partir da anamnese mais recente do usuário logado."""
    return workout_service.gerar_e_salvar_treino(user_id)