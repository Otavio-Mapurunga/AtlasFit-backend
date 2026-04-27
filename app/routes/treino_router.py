from fastapi import APIRouter, HTTPException
from app.repositories import workout_repository

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