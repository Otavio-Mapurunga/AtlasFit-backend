from app.config import supabase

def buscar_exercicios():
    """Busca todos os exercícios cadastrados no Supabase."""
    response = supabase.table("exercicios").select("name","id","primaryMuscles").execute()
    return response.data
def salvar_treino(id_aluno: str, nome_treino: dict | None = None):
    response=supabase.table("treinos").insert({
        "id_aluno":id_aluno,
        "nome_treino":nome_treino,
        "objetivo":"gerado automaticamente",
    }).execute()
    #sempre usar () para executar um requerimento ou ação, sem isso não funciona
    return response.data[0]["id"]

def salvar_exercicio_no_treino(id_treino:str,id_exercicio:str,series:int,repeticoes:str):
    supabase.table("treino_exercicios").insert({
        "id_treino":id_treino,
        "id_exercicio":id_exercicio,
        "series":series,
        "repeticoes":repeticoes
    }).execute()
    return 