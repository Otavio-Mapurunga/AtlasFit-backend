from fastapi import APIRouter
import json
from fastapi import HTTPException
from rapidfuzz import process,fuzz
from app.services.groq_service import (
    GroqServiceError,
    GroqTemporaryUnavailableError,#type: ignore
    gerar_treino,
)
from app.repositories.exercicios_repository import (
    buscar_exercicios,
    salvar_treino,
    salvar_dia_treino,
    salvar_exercicio_no_treino,
)
from app.schemas.treino_schemas import AlunoRequest,TreinoResponse
from app.repositories.exercicios_repository import buscar_exercicios, salvar_treino,salvar_exercicio_no_treino

#router vai servir para facilitar a troca de url do site. prefixo /ia serve para deixar a url mais padronizada e limpa quando for utilizado algo de ia
router = APIRouter(prefix="/ia")

@router.get("/test")
def testar_ai():
    try:
        resposta = gerar_treino("diga apenas: api funcionando")
    except GroqTemporaryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except GroqServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"resposta": resposta}
#geração de prompt com base nos dados recibos da classe alunorequest
@router.post("/generate-workout",response_model=TreinoResponse)
def treino_gerado(aluno: AlunoRequest):
    exercicios = buscar_exercicios()
    lista_exercicios = "\n".join([f"- {e['name']}" for e in exercicios])#type: ignore
    mapa_exercicio = {e['name']: e['id'] for e in exercicios}#type: ignore
    nomes = list(mapa_exercicio.keys())
    agacha = [n for n in nomes if "gach" in n.lower()]
    print(f"[debug] Exercícios com 'agach' no nome: {agacha}")

    prompt = f"""Responda com um JSON válido, sem explicações, sem texto antes ou depois, sem blocos markdown.
        Crie exatamente {aluno.dias_treino} treinos diferentes, nomeados sequencialmente começando em A.
        Use nomes de exercícios em PORTUGUÊS.
        Formato obrigatório:
        {{
        "treino": {{
            "A": [
            {{"exercicio":"nome do exercicio","series":4,"reps":"8-10"}}
            ]
        }}
        }}

        Dados do aluno:
        Idade: {aluno.idade}
        Peso: {aluno.peso}
        Altura: {aluno.altura}
        Objetivo: {aluno.objetivo}
        Nível: {aluno.nivel}
        Dias de treino por semana: {aluno.dias_treino}
        """

    try:
        resposta = gerar_treino(prompt)
    except GroqTemporaryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except GroqServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    resposta = resposta.replace("```json", "").replace("```", "").strip()
    print(f"Resposta da IA: {resposta}")

    try:
        dados_json = json.loads(resposta)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="A IA retornou um JSON inválido.")

    treino_validado = TreinoResponse(**dados_json)
    id_aluno = "522a1f07-9408-4f3f-b90c-783862846f3e"

    # 1. salva o treino principal
    try:
        id_treino = salvar_treino(id_aluno)#erro
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar treino: {exc}") from exc

    # 2. para cada dia (A, B, C...) salva o dia e seus exercícios
    for ordem_dia, (nome_dia, exercicios_do_dia) in enumerate(treino_validado.treino.items(), start=1):
        try:
            id_dia = salvar_dia_treino(id_treino, nome_dia, ordem_dia)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar dia '{nome_dia}': {exc}") from exc

        for ordem_ex, ex in enumerate(exercicios_do_dia, start=1):
            # busca exata primeiro
            id_exercicio = mapa_exercicio.get(ex.exercicio)

            # se não achou, tenta fuzzy com score mais baixo
            if not id_exercicio:
                resultado = process.extractOne(
                    ex.exercicio,
                    mapa_exercicio.keys(),
                    scorer=fuzz.WRatio,
                    score_cutoff=55 
                )
                if resultado:
                    nome_encontrado = resultado[0]
                    print(f"[fuzzy] '{ex.exercicio}' → '{nome_encontrado}'")
                    id_exercicio = mapa_exercicio[nome_encontrado]
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Exercício '{ex.exercicio}' não encontrado no banco."
                    )

            try:
                salvar_exercicio_no_treino(
                    id_dia_treino=id_dia,
                    id_exercicio=id_exercicio,
                    series=ex.series,
                    repeticoes=ex.reps,
                    ordem=ordem_ex,
                )
            except Exception as exc:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao salvar exercício '{ex.exercicio}': {exc}"
                ) from exc

    return treino_validado
    
