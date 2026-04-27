from fastapi import APIRouter, HTTPException
from app.repositories import workout_repository

## isso foi eu 
from app.schemas.treino_schemas import ProgressaoResponse, TreinoInput
from app.services.progressao_service import calcular_progressao, carga_sugerida, validar_treino

@router.post("/calcular", response_model=ProgressaoResponse)
def calcular_treino(data: TreinoInput):
    try:
        nova = calcular_progressao(data.carga_atual, data.nivel)
        sugerida = carga_sugerida(data.carga_atual, data.nivel, data.fadiga)
        validacao = validar_treino(data.nivel, data.treinos_semana, data.reps)
        return {"nova_carga": nova, "carga_sugerida": sugerida, "validacao": validacao}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
## aqui já não é mais



router = APIRouter(prefix="/treinos", tags=["Treinos"])

# id_aluno ainda hardcoded — será substituído pelo JWT do Sam
ID_ALUNO_TEMP = "522a1f07-9408-4f3f-b90c-783862846f3e"

@router.get("/")
def listar_treinos():
    """Lista todos os treinos do usuário logado."""
    treinos = workout_repository.buscar_treinos_do_aluno(ID_ALUNO_TEMP)
    return {"treinos": treinos, "total": len(treinos)}


@router.get("/{id_treino}")
def detalhar_treino(id_treino: str):
    """Retorna um treino completo com dias e exercícios."""
    treino = workout_repository.buscar_treino_por_id(id_treino, ID_ALUNO_TEMP)

    if not treino:
        raise HTTPException(
            status_code=404,
            detail="Treino não encontrado."
        )

    return treino

@router.delete("/{id_treino}")
def deletar_treino(id_treino: str):
    """Deleta um treino do usuário logado."""
    treino = workout_repository.buscar_treino_por_id(id_treino, ID_ALUNO_TEMP)

    if not treino:
        raise HTTPException(
            status_code=404,
            detail="Treino não encontrado."
        )

    deletado = workout_repository.deletar_treino(id_treino, ID_ALUNO_TEMP)

    if not deletado:
        raise HTTPException(
            status_code=500,
            detail="Erro ao deletar treino."
        )

    return {"mensagem": "Treino deletado com sucesso.", "id_treino": id_treino}
