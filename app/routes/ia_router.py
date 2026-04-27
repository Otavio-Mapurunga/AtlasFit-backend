from fastapi import APIRouter, HTTPException
from app.services.groq_service import GroqServiceError, GroqTemporaryUnavailableError, gerar_treino
from app.services import workout_service
from app.schemas.treino_schemas import AlunoRequest, TreinoResponse

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
def treino_gerado(aluno: AlunoRequest):
    # id_aluno ainda hardcoded — será substituído pelo JWT do Sam
    ID_ALUNO_TEMP = "522a1f07-9408-4f3f-b90c-783862846f3e"

    return workout_service.gerar_e_salvar_treino(aluno, ID_ALUNO_TEMP)