from app.config import supabase

def buscar_exercicios():
    """Busca todos os exercícios cadastrados no Supabase."""
    response = supabase.table("exercicios").select("name","id","primaryMuscles").execute()
    return response.data
