from app.config import supabase

def buscar_exercicios():
    """Busca todos os exercícios cadastrados no Supabase."""
    response = supabase.table("exercicios").select("name","id","primaryMuscles").execute()
    return response.data
def salvar_treino(usuario_id: str, _treino: dict | None = None):
    response=supabase.table("treinos").insert({
        "id_aluno":usuario_id,
        "nome_treino":"treino IA",
        "objetivo":"gerado automaticamente",
    }).execute()
    #sempre usar () para executar um requerimento ou ação, sem isso não funciona
    return response.data
