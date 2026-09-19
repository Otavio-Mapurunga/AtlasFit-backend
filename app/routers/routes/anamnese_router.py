from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user_id
from app.repositories import anamnese_repository
from app.schemas.anamnese_schemas import AnamneseCreate, AnamneseResponse

router = APIRouter(prefix="/anamnese", tags=["Anamnese"])


@router.post("/", response_model=AnamneseResponse)
def criar_anamnese(data: AnamneseCreate, user_id: str = Depends(get_current_user_id)):
    return anamnese_repository.criar_anamnese(user_id, data.dict())


@router.get("/", response_model=AnamneseResponse)
def buscar_minha_anamnese(user_id: str = Depends(get_current_user_id)):
    anamnese = anamnese_repository.buscar_anamnese_mais_recente(user_id)
    if not anamnese:
        raise HTTPException(status_code=404, detail="Nenhuma anamnese encontrada para este aluno.")
    return anamnese