from app.config import supabase

def buscar_treinos_do_aluno(id_aluno: str) -> list:
    response = (
        supabase.table("treinos")
        .select("*")
        .eq("id_aluno", id_aluno)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data or []


def buscar_treino_por_id(id_treino: str, id_aluno: str) -> dict | None:
    response = (
        supabase.table("treinos")
        .select("*, treino_dias(*, treino_exercicios(*, exercicios(name, primaryMuscles)))")
        .eq("id_treino", id_treino)
        .eq("id_aluno", id_aluno)
        .execute()
    )
    return response.data[0] if response.data else None#type:ignore


def deletar_treino(id_treino: str, id_aluno: str) -> bool:
    response = (
        supabase.table("treinos")
        .delete()
        .eq("id_treino", id_treino)
        .eq("id_aluno", id_aluno)
        .execute()
    )
    return bool(response.data)