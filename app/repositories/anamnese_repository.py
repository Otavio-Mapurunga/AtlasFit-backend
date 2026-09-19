from sqlalchemy import text
from app.database import engine, insert_one


def criar_anamnese(id_aluno: str, data: dict) -> dict:
    row = insert_one("anamnse", {
        "id_aluno": id_aluno,
        "altura": data["altura"],
        "peso": data["peso"],
        "sexo": data["sexo"],
        "objetivo": data["objetivo"],
        "experiencia": data["experiencia"],
        "lesoes": data.get("lesoes"),
        "dias_treino": data.get("dias_treino"),
        "idade": data["idade"],
        "observacoes_medicas": data["observacoes_medicas"],
        "equipamentos": data.get("equipamentos"),
        "preferencias": data["preferencias"],
    }, returning="*")

    if not row:
        raise ValueError("Inserção em 'anamnse' não retornou dados.")

    return row


def buscar_anamnese_mais_recente(id_aluno: str) -> dict | None:
    query = text("""
        SELECT * FROM anamnse
        WHERE id_aluno = :id_aluno
        ORDER BY created_at DESC
        LIMIT 1
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"id_aluno": id_aluno})
        row = result.mappings().first()
        return dict(row) if row else None