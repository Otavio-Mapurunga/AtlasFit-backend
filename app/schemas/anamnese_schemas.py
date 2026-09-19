import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class AnamneseCreate(BaseModel):
    altura: int = Field(..., gt=0, description="Altura em cm")
    peso: float = Field(..., gt=0, description="Peso em kg")
    sexo: str
    objetivo: List[str]
    experiencia: str
    lesoes: Optional[List[str]] = None
    dias_treino: Optional[int] = None
    idade: int = Field(..., gt=0)
    observacoes_medicas: str
    equipamentos: Optional[List[str]] = None
    preferencias: str


class AnamneseResponse(AnamneseCreate):
    id_anamnese: uuid.UUID
    id_aluno: uuid.UUID
    created_at: datetime