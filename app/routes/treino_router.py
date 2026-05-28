from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.repositories import workout_repository
from app.auth.dependencies import get_current_user_id, get_token_payload
from app.auth.jwt import create_access_token
from app.config import JWT_EXPIRES_MINUTES

from app.schemas.treino_schemas import ProgressaoResponse, TreinoInput

# O import de progressao_service foi reativado e o arquivo app/services/progressao_service.py deve conter as funções.
from app.services.progressao_service import calcular_progressao, carga_sugerida, validar_treino

router = APIRouter(prefix="/treinos", tags=["Treinos"])


class ProgressaoWithToken(ProgressaoResponse):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/calcular", response_model=ProgressaoWithToken)
def calcular_treino(data: TreinoInput, user_id: str = Depends(get_current_user_id)):
    try:
        nova = calcular_progressao(data.carga_atual, data.nivel)
        sugerida = carga_sugerida(data.carga_atual, data.nivel, data.fadiga)
        validacao = validar_treino(data.nivel, data.treinos_semana, data.reps)
        resultado = {"nova_carga": nova, "carga_sugerida": sugerida, "validacao": validacao}

        payload = {
            "sub": user_id,
            "last_input": data.dict(),
            "last_result": resultado,
        }
        expires = timedelta(minutes=JWT_EXPIRES_MINUTES)
        token = create_access_token(data=payload, expires_delta=expires)

        return {
            **resultado,
            "access_token": token,
            "token_type": "bearer",
            "expires_in": JWT_EXPIRES_MINUTES * 60,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/ultimo-calculo", response_model=ProgressaoResponse)
def ultimo_calculo(token_payload: dict = Depends(get_token_payload)):
    resultado = token_payload.get("last_result")
    if not resultado:
        raise HTTPException(status_code=404, detail="Nenhum cálculo salvo no token.")
    return resultado


@router.get("/ultimo-input", response_model=TreinoInput)
def ultimo_input(token_payload: dict = Depends(get_token_payload)):
    ultimo = token_payload.get("last_input")
    if not ultimo:
        raise HTTPException(status_code=404, detail="Nenhum registro anterior no token.")
    return ultimo


@router.get("/")
def listar_treinos(user_id: str = Depends(get_current_user_id)):
    """Lista todos os treinos do usuário logado."""
    treinos = workout_repository.buscar_treinos_do_aluno(user_id)
    return {"treinos": treinos, "total": len(treinos)}


@router.get("/{id_treino}")
def detalhar_treino(id_treino: str, user_id: str = Depends(get_current_user_id)):
    """Retorna um treino completo com dias e exercícios."""
    treino = workout_repository.buscar_treino_por_id(id_treino, user_id)

    if not treino:
        raise HTTPException(
            status_code=404,
            detail="Treino não encontrado."
        )
    return treino


@router.delete("/{id_treino}")
def deletar_treino(id_treino: str, user_id: str = Depends(get_current_user_id)):
    """Deleta um treino do usuário logado."""
    # A busca inicial garante que o treino pertence ao usuário antes de deletar.
    treino = workout_repository.buscar_treino_por_id(id_treino, user_id)

    if not treino:
        raise HTTPException(
            status_code=404,
            detail="Treino não encontrado."
        )

    deletado = workout_repository.deletar_treino(id_treino, user_id)

    if not deletado:
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar treino."
        )

    return {"mensagem": "Treino deletado com sucesso.", "id_treino": id_treino}
