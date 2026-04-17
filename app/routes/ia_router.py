from fastapi import APIRouter
from pydantic import BaseModel
import json
from fastapi import HTTPException
from app.services.gemini_service import gerar_treino
from app.schemas.treino_schemas import AlunoRequest,TreinoResponse
from app.repositories.exercicios_repository import buscar_exercicios, salvar_treino,salvar_exercicio_no_treino

#router vai servir para facilitar a troca de url do site. prefixo /ia serve para deixar a url mais padronizada e limpa quando for utilizado algo de ia
router = APIRouter(prefix="/ia")

@router.get("/test")
def testar_ai():

    resposta = gerar_treino("diga apenas: api funcionando")

    return {"resposta": resposta}
#geração de prompt com base nos dados recibos da classe alunorequest
@router.post("/generate-workout",response_model=TreinoResponse)
def treino_gerado(aluno: AlunoRequest):
    exercicios = buscar_exercicios()
    lista_exercicios="\n".join([f"- {e['name']}" for e in exercicios])#type: ignore
    mapa_exercicio={e['name']: e['id'] for e in exercicios}#type: ignore
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
    Use APENAS nomes EXATOS da lista abaixo.
    NÃO modifique, NÃO invente, NÃO traduza.
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
    resposta=resposta.replace("```json","").replace("```","")# type: ignore
    resposta=resposta.strip()
    print(f"Resposta da i.a:",resposta)
    try:
      dados_json=json.loads(resposta)
    except json.JSONDecodeError:
       raise HTTPException(status_code=400, detail="A i.a retornou um JSON invalido")
    treino_validado=TreinoResponse(**dados_json)
    id_aluno="522a1f07-9408-4f3f-b90c-783862846f3e"
    for nome_treino,exercicios in treino_validado.treino.items():
       id_treino = salvar_treino(id_aluno, nome_treino)

       for ex in exercicios:
          id_execercicio=mapa_exercicio.get(ex.exercicio)
         
          if not id_execercicio:
             raise HTTPException(
               status_code=400,
               detail=f"Não foi possivel encontrar o id do exercicio {ex.exercicio}"
             )
          salvar_exercicio_no_treino(
             id_treino=id_treino, # type: ignore
             id_exercicio=id_execercicio, # type: ignore
             series=ex.series,
             repeticoes=ex.reps
          )

    return treino_validado
    
