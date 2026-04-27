import json
from rapidfuzz import process, fuzz
from fastapi import HTTPException

from app.services.groq_service import (
    gerar_treino,
    GroqServiceError,
    GroqTemporaryUnavailableError,
)
from app.repositories.exercicios_repository import (
    buscar_exercicios,
    salvar_treino,
    salvar_dia_treino,
    salvar_exercicio_no_treino,
)
from app.schemas.treino_schemas import AlunoRequest, TreinoResponse

import unicodedata

def _normalizar(texto: str) -> str:
    """Remove acentos e coloca em minúsculo para comparação."""
    return unicodedata.normalize("NFD", texto)\
        .encode("ascii", "ignore")\
        .decode("utf-8")\
        .lower()\
        .strip()


def _montar_prompt(aluno: AlunoRequest) -> str:
    return f"""Responda com um JSON válido, sem explicações, sem texto antes ou depois, sem blocos markdown.
    Crie exatamente {aluno.dias_treino} treinos diferentes, nomeados sequencialmente começando em A.
    Use APENAS exercícios de musculação com equipamentos (halteres, barra, máquinas, cabos).
    NÃO inclua atividades como corrida, jiu-jitsu, natação ou qualquer esporte.
    Use nomes de exercícios em PORTUGUÊS.
    Formato obrigatório:
    {{
      "treino": {{
        "A": [
          {{"exercicio": "nome do exercicio", "series": 4, "reps": "8-10"}}
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


def _parse_resposta_ia(resposta_bruta: str) -> TreinoResponse:
    resposta_limpa = resposta_bruta.replace("```json", "").replace("```", "").strip()

    try:
        dados_json = json.loads(resposta_limpa)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="A IA retornou um JSON inválido."
        )

    return TreinoResponse(**dados_json)


def _resolver_exercicio(nome: str, mapa: dict) -> str:
    """
    Tenta encontrar o exercício no banco.
    1. Busca exata
    2. Busca exata normalizada (sem acento)
    3. Fuzzy matching com score >= 75
    """
    # 1. busca exata
    id_exercicio = mapa.get(nome)
    if id_exercicio:
        return id_exercicio

    # 2. normaliza tudo e tenta busca exata sem acento
    nome_normalizado = _normalizar(nome)
    mapa_normalizado = {_normalizar(k): v for k, v in mapa.items()}

    id_exercicio = mapa_normalizado.get(nome_normalizado)
    if id_exercicio:
        print(f"[norm] '{nome}' → encontrado por normalização")
        return id_exercicio

    # 3. fuzzy com score mais alto e base normalizada
    resultado = process.extractOne(
        nome_normalizado,
        mapa_normalizado.keys(),
        scorer=fuzz.WRatio,
        score_cutoff=75
    )

    if resultado:
        nome_encontrado = resultado[0]
        id_exercicio = mapa_normalizado[nome_encontrado]
        print(f"[fuzzy] '{nome}' → '{nome_encontrado}' (score: {resultado[1]:.0f})")
        return id_exercicio

    # 4. não encontrou nada confiável
    raise HTTPException(
        status_code=400,
        detail=f"Exercício '{nome}' não encontrado no banco. Revise o nome ou adicione ao cadastro."
    )


def _salvar_treino_completo(id_aluno: str, treino: TreinoResponse, mapa: dict) -> None:

    try:
        id_treino = salvar_treino(id_aluno)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao salvar treino: {exc}"
        ) from exc

    for ordem_dia, (nome_dia, exercicios_do_dia) in enumerate(treino.treino.items(), start=1):
        try:
            id_dia = salvar_dia_treino(id_treino, nome_dia, ordem_dia)
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao salvar dia '{nome_dia}': {exc}"
            ) from exc

        for ordem_ex, ex in enumerate(exercicios_do_dia, start=1):
            id_exercicio = _resolver_exercicio(ex.exercicio, mapa)

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


def gerar_e_salvar_treino(aluno: AlunoRequest, id_aluno: str) -> TreinoResponse:

    exercicios = buscar_exercicios()
    mapa_exercicio = {e["name"]: e["id"] for e in exercicios}  # type: ignore

    # 2. monta prompt e chama IA
    prompt = _montar_prompt(aluno)

    try:
        resposta_bruta = gerar_treino(prompt)
    except GroqTemporaryUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except GroqServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    treino_validado = _parse_resposta_ia(resposta_bruta)

    _salvar_treino_completo(id_aluno, treino_validado, mapa_exercicio)

    return treino_validado