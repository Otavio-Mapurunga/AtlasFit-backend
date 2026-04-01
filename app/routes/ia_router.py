from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.services.gemini_service import gerar_treino
from app.schemas.treino_schemas import AlunoRequest,TreinoResponse

#router vai servir para facilitar a troca de url do site. prefixo /ia serve para deixar a url mais padronizada e limpa quando for utilizado algo de ia
router = APIRouter(prefix="/ia")

@router.get("/test")
def testar_ai():

    resposta = gerar_treino("diga apenas: api funcionando")

    return {"resposta": resposta}
#geração de prompt com base nos dados recibos da classe alunorequest
@router.post("/generate-workout",response_model=TreinoResponse)
def trieno_gerado(aluno: AlunoRequest):
    prompt= f"""
    Crie um treino baseado nos dados:
    Idade:{aluno.idade}
    Peso:{aluno.peso}
    Altura:{aluno.altura}
    Objetivo:{aluno.objetivo}
    nivel:{aluno.nivel}
    dias de trieno por semana:{aluno.dias_treino}

    {{
      "treino": {{
        "A": [
          {{"exercicio":"Supino","series":4,"reps":"8-10"}}
        ]
      }}
    }}"""

    resposta=gerar_treino(prompt)
    dados_json=json.loads(resposta)
    treino_validado=TreinoResponse(**dados_json)
    return treino_validado
