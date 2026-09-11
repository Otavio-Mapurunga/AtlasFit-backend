from sqlalchemy import text
from app.database import engine, insert_one, insert_many


def registrar_execucao(id_aluno: str, id_treino: str, duracao: int | None) -> str:
    row = insert_one("execucao", {
        "id_aluno": id_aluno,
        "id_treino": id_treino,
        "duracao": duracao,
    }, returning="id_execucao")

    if not row:
        raise ValueError("Inserção em 'execucao' não retornou dados.")

    return str(row["id_execucao"])


def registrar_exercicios_execucao(id_execucao: str, exercicios: list) -> None:
    rows = [
        {
            "id_execucao": id_execucao,
            "id": ex["id"],
            "series_realizadas": ex.get("series_realizadas"),
            "reps_realizadas": ex.get("reps_realizadas"),
            "peso_utilizado": ex.get("peso_utilizado"),
        }
        for ex in exercicios
    ]
    insert_many("execucao_exercicio", rows)


def buscar_execucao_por_id(id_execucao: str, id_aluno: str) -> dict | None:
    query = text("""
        SELECT
            e.*,
            COALESCE(
                json_agg(
                    json_build_object(
                        'id', ee.id,
                        'series_realizadas', ee.series_realizadas,
                        'reps_realizadas', ee.reps_realizadas,
                        'peso_utilizado', ee.peso_utilizado,
                        'exercicios', json_build_object('name', ex.name, 'primaryMuscles', ex."primaryMuscles")
                    )
                ) FILTER (WHERE ee.id IS NOT NULL), '[]'
            ) AS execucao_exercicio
        FROM execucao e
        LEFT JOIN execucao_exercicio ee ON ee.id_execucao = e.id_execucao
        LEFT JOIN exercicios ex ON ex.id = ee.id
        WHERE e.id_execucao = :id_execucao AND e.id_aluno = :id_aluno
        GROUP BY e.id_execucao
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"id_execucao": id_execucao, "id_aluno": id_aluno})
        row = result.mappings().first()
        return dict(row) if row else None


def buscar_historico_aluno(id_aluno: str) -> list:
    query = text("""
        SELECT
            e.*,
            COALESCE(
                json_agg(
                    json_build_object(
                        'id', ee.id,
                        'series_realizadas', ee.series_realizadas,
                        'reps_realizadas', ee.reps_realizadas,
                        'peso_utilizado', ee.peso_utilizado,
                        'exercicios', json_build_object('name', ex.name, 'primaryMuscles', ex."primaryMuscles")
                    )
                ) FILTER (WHERE ee.id IS NOT NULL), '[]'
            ) AS execucao_exercicio
        FROM execucao e
        LEFT JOIN execucao_exercicio ee ON ee.id_execucao = e.id_execucao
        LEFT JOIN exercicios ex ON ex.id = ee.id
        WHERE e.id_aluno = :id_aluno
        GROUP BY e.id_execucao
        ORDER BY e.data_execucao DESC
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"id_aluno": id_aluno})
        return [dict(r) for r in result.mappings().all()]