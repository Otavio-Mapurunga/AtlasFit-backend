from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.services.gemini_service import gerar_treino
from app.schemas.treino_schemas import AlunoRequest,TreinoResponse
from app.repositories.exercicios_repository import buscar_exercicios

#router vai servir para facilitar a troca de url do site. prefixo /ia serve para deixar a url mais padronizada e limpa quando for utilizado algo de ia
router = APIRouter(prefix="/ia")

@router.get("/test")
def testar_ai():

    resposta = gerar_treino("diga apenas: api funcionando")

    return {"resposta": resposta}
#geração de prompt com base nos dados recibos da classe alunorequest
@router.post("/generate-workout",response_model=TreinoResponse)
def trieno_gerado(aluno: AlunoRequest):
    exercicios = buscar_exercicios()
    lista_exercicios="\n".join([f"- {e['name']}" for e in exercicios])
    prompt= f""" 
    Responda com um JSON valido
    sem explicações
    não crie textos antes ou depois 
    Crie exatamente {aluno.dias_treino} treinos diferentes.
    Nomeie-os sequencialmente começando em A.
    formato obrigatorio:
    {{
      "treino": {{
        "A": [
          {{"exercicio":"Supino","series":4,"reps":"8-10"}}
        ]
      }}
    }}
    Use apenas os exercicios dessa lista:
    {lista_exercicios}

    Crie um treino baseado nos dados:
    Idade:{aluno.idade}
    Peso:{aluno.peso}
    Altura:{aluno.altura}
    Objetivo:{aluno.objetivo}
    nivel:{aluno.nivel}
    dias de trieno por semana:{aluno.dias_treino}

    """

    resposta=gerar_treino(prompt)
    resposta=resposta.replace("```json","").replace("```","")
    resposta=resposta.strip()
    print(f"Resposta da i.a:",resposta)
    try:
      dados_json=json.loads(resposta)
    except json.JSONDecodeError:
        return {"Error : I.A retornou um json inválido"}
    treino_validado=TreinoResponse(**dados_json)
    
    return treino_validado
    
