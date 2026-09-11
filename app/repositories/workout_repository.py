from sqlalchemy import text
from app.database import engine


def buscar_treinos_do_aluno(id_aluno: str) -> list:
    query = text("SELECT * FROM treinos WHERE id_aluno = :id_aluno ORDER BY data_criacao DESC")
    with engine.connect() as conn:
        result = conn.execute(query, {"id_aluno": id_aluno})
        return [dict(r) for r in result.mappings().all()]

def buscar_treino_por_id(id_treino: str, id_aluno: str) -> dict | None:
    query = text("""
        SELECT
            t.*,
            COALESCE(
                json_agg(
                    json_build_object(
                        'id_dia', td.id_dia,
                        'nome_dia', td.nome_dia,
                        'ordem', td.ordem,
                        'treino_exercicios', td.exercicios
                    )
                    ORDER BY td.ordem
                ) FILTER (WHERE td.id_dia IS NOT NULL), '[]'
            ) AS treino_dias
        FROM treinos t
        LEFT JOIN (
            SELECT
                d.id_dia, d.id_treino, d.nome_dia, d.ordem,
                COALESCE(
                    json_agg(
                        json_build_object(
                            'id', te.id, 'series', te.series, 'repeticoes', te.repeticoes, 'ordem', te.ordem,
                            'exercicios', json_build_object('name', ex.name, 'primaryMuscles', ex."primaryMuscles")
                        ) ORDER BY te.ordem
                    ) FILTER (WHERE te.id IS NOT NULL), '[]'
                ) AS exercicios
            FROM treino_dias d
            LEFT JOIN treino_exercicios te ON te.id_dia_treino = d.id_dia
            LEFT JOIN exercicios ex ON ex.id = te.id
            GROUP BY d.id_dia
        ) td ON td.id_treino = t.id_treino
        WHERE t.id_treino = :id_treino AND t.id_aluno = :id_aluno
        GROUP BY t.id_treino
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"id_treino": id_treino, "id_aluno": id_aluno})
        row = result.mappings().first()
        return dict(row) if row else None


def deletar_treino(id_treino: str, id_aluno: str) -> bool:
    query = text("DELETE FROM treinos WHERE id_treino = :id_treino AND id_aluno = :id_aluno RETURNING id_treino")
    with engine.begin() as conn:
        result = conn.execute(query, {"id_treino": id_treino, "id_aluno": id_aluno})
        return result.first() is not None