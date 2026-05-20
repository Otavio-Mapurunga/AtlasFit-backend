from pydantic import BaseModel
from typing import List, Optional

class ExecucaoExercicioInput(BaseModel):
    id: str  # id do exercicio, ex: "3_4_Sit-Up"
    series_realizadas: Optional[int] = None
    reps_realizadas: Optional[int] = None
    peso_utilizado: Optional[int] = None

class ExecucaoCreate(BaseModel):
    id_treino: str
    id_aluno: str  # temporário até Sam integrar o JWT
    duracao: Optional[int] = None
    exercicios: List[ExecucaoExercicioInput]

class ExecucaoResponse(BaseModel):
    id_execucao: str
    id_aluno: str
    id_treino: str
    data_execucao: Optional[str] = None
    duracao: Optional[int] = None
    exercicios: List[dict]