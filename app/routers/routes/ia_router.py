from fastapi import APIRouter, Depends, HTTPException
from app.services.groq_service import GroqServiceError, GroqTemporaryUnavailableError, gerar_treino
from app.services import workout_service
from app.schemas.treino_schemas import AlunoRequest, TreinoResponse
from app.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/ia")

# rota de teste da IA — mantida para debug
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
def treino_gerado(aluno: AlunoRequest, user_id: str = Depends(get_current_user_id)):
    """Gera e salva um novo treino para o usuário logado."""
    return workout_service.gerar_e_salvar_treino(aluno, user_id)