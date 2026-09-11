from sqlalchemy import text
from app.database import engine, insert_one


def buscar_exercicios():
    query = text('SELECT name, id, "primaryMuscles" FROM exercicios')
    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(r) for r in result.mappings().all()]


def salvar_treino(id_aluno: str, objetivo: str = "gerado automaticamente") -> str:
    row = insert_one("treinos", {
        "id_aluno": id_aluno,
        "nome_treino": "Treino gerado por IA",
        "objetivo": objetivo,
    }, returning="id_treino")

    if not row:
        raise ValueError("Inserção em 'treinos' não retornou dados.")

    return str(row["id_treino"])


def salvar_dia_treino(id_treino: str, nome_dia: str, ordem: int) -> str:
    row = insert_one("treino_dias", {
        "id_treino": id_treino,
        "nome_dia": nome_dia,
        "ordem": ordem,
    }, returning="id_dia")

    if not row:
        raise ValueError(f"Inserção em 'treino_dias' não retornou dados para o dia '{nome_dia}'.")

    return str(row["id_dia"])


def salvar_exercicio_no_treino(id_dia_treino: str, id_exercicio: str, series: int, repeticoes: str, ordem: int):
    insert_one("treino_exercicios", {
        "id_dia_treino": id_dia_treino,
        "id": id_exercicio,
        "series": series,
        "repeticoes": repeticoes,
        "ordem": ordem,
    })