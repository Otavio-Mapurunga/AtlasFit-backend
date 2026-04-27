from app.config import supabase

def buscar_exercicios():
    response = supabase.table("exercicios").select("name", "id", "primaryMuscles").execute()
    return response.data

def salvar_treino(id_aluno: str, objetivo: str = "gerado automaticamente") -> str:
    response = supabase.table("treinos").insert({
        "id_aluno": id_aluno,
        "nome_treino": "Treino gerado por IA",
        "objetivo": objetivo,
    }).execute()

    if not response.data:
        raise ValueError("Inserção em 'treinos' não retornou dados.")

    return str(response.data[0]["id_treino"])#type:ignore


def salvar_dia_treino(id_treino: str, nome_dia: str, ordem: int) -> str:
    response = supabase.table("treino_dias").insert({
        "id_treino": id_treino,
        "nome_dia": nome_dia,
        "ordem": ordem,
    }).execute()

    if not response.data:
        raise ValueError(f"Inserção em 'treino_dias' não retornou dados para o dia '{nome_dia}'.")

    return str(response.data[0]["id_dia"]) #type:ignore

def salvar_exercicio_no_treino(id_dia_treino: str, id_exercicio: str, series: int, repeticoes: str, ordem: int):
    supabase.table("treino_exercicios").insert({
        "id_dia_treino": id_dia_treino,
        "id": id_exercicio,
        "series": series,
        "repeticoes": repeticoes,
        "ordem": ordem,
    }).execute() 
