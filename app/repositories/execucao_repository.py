from app.config import supabase

def registrar_execucao(id_aluno: str, id_treino: str, duracao: int | None) -> str:
    response = (
        supabase.table("execucao")
        .insert({
            "id_aluno": id_aluno,
            "id_treino": id_treino,
            "duracao": duracao,
        })
        .execute()
    )
def registrar_execucao(id_aluno: str, id_treino: str, duracao: int | None) -> str:
    response = (
        supabase.table("execucao")
        .insert({
            "id_aluno": id_aluno,
            "id_treino": id_treino,
            "duracao": duracao,
        })
        .execute()
    )

    if not response.data:
        raise ValueError("Inserção em 'execucao' não retornou dados.")

    return str(response.data[0]["id_execucao"])

    if not response.data:
        raise ValueError("Inserção em 'execucao' não retornou dados.")

    return str(response.data[0]["id_execucao"])


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
    supabase.table("execucao_exercicio").insert(rows).execute()


def buscar_execucao_por_id(id_execucao: str, id_aluno: str) -> dict | None:
    response = (
        supabase.table("execucao")
        .select("*, execucao_exercicio(*, exercicios(name, primaryMuscles))")
        .eq("id_execucao", id_execucao)
        .eq("id_aluno", id_aluno)
        .execute()
    )
    return response.data[0] if response.data else None


def buscar_historico_aluno(id_aluno: str) -> list:
    response = (
        supabase.table("execucao")
        .select("*, execucao_exercicio(*, exercicios(name, primaryMuscles))")
        .eq("id_aluno", id_aluno)
        .order("data_execucao", desc=True)
        .execute()
    )
    return response.data or []