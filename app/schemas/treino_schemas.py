from pydantic import BaseModel
from typing import List,Dict
class AlunoRequest(BaseModel):
    idade:int
    peso:float
    altura:float
    objetivo:str
    nivel:str
    dias_treino:int

class Exercicio(BaseModel):
    exercicio:str
    series:int
    reps:str

class TreinoResponse(BaseModel):
    treino:Dict[str,List[Exercicio]]

class TreinoCreate(BaseModel):
    usuario_id:str
    treino:Dict[str,List[Exercicio]]