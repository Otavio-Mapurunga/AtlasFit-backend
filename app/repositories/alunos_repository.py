import bcrypt
from sqlalchemy import text
from app.database import engine, insert_one


def criar_aluno(nome: str, email: str, senha: str) -> dict:
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    row = insert_one("alunos", {
        "nome": nome,
        "email": email,
        "senha_hash": senha_hash,
    }, returning="id_aluno, nome, email")

    if not row:
        raise ValueError("Inserção em 'alunos' não retornou dados.")

    return dict(row)


def buscar_aluno_por_email(email: str) -> dict | None:
    query = text("SELECT id_aluno, nome, email, senha_hash FROM alunos WHERE email = :email")
    with engine.connect() as conn:
        result = conn.execute(query, {"email": email})
        row = result.mappings().first()
        return dict(row) if row else None


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))