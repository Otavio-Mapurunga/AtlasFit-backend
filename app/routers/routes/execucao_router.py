from fastapi import APIRouter, Depends, HTTPException
from app.schemas.execucao_schemas import ExecucaoCreate, ExecucaoResponse
from app.auth.dependencies import get_current_user_id
from app.repositories.execucao_repository import (
    registrar_execucao,
    registrar_exercicios_execucao,
    buscar_execucao_por_id,
    buscar_historico_aluno,
)

router = APIRouter(prefix="/execucao", tags=["Execução"])


@router.post("/", response_model=dict)
def registrar_sessao(payload: ExecucaoCreate, user_id: str = Depends(get_current_user_id)):
    try:
        id_execucao = registrar_execucao(
            id_aluno=user_id,
            id_treino=payload.id_treino,
            duracao=payload.duracao,
        )
        exercicios_dict = [ex.model_dump() for ex in payload.exercicios]
        registrar_exercicios_execucao(id_execucao, exercicios_dict)

        return {"id_execucao": id_execucao, "mensagem": "Sessão registrada com sucesso."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/historico", response_model=list)
def historico_aluno(user_id: str = Depends(get_current_user_id)):
    return buscar_historico_aluno(user_id)


@router.get("/{id_execucao}", response_model=dict)
def detalhe_execucao(id_execucao: str, user_id: str = Depends(get_current_user_id)):
    execucao = buscar_execucao_por_id(id_execucao, user_id)
    if not execucao:
        raise HTTPException(status_code=404, detail="Execução não encontrada.")
    return execucao