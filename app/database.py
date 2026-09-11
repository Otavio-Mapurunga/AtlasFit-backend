from sqlalchemy import create_engine, text
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)


def insert_one(table: str, data: dict, returning: str = "*") -> dict | None:
    """Espelha o comportamento de supabase.table(x).insert(dict).execute()"""
    columns = ", ".join(data.keys())
    placeholders = ", ".join(f":{k}" for k in data.keys())
    query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING {returning}")
    with engine.begin() as conn:
        result = conn.execute(query, data)
        row = result.mappings().first()
        return dict(row) if row else None


def insert_many(table: str, rows: list[dict]) -> None:
    """Espelha supabase.table(x).insert([...]).execute() para múltiplas linhas"""
    if not rows:
        return
    columns = ", ".join(rows[0].keys())
    placeholders = ", ".join(f":{k}" for k in rows[0].keys())
    query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")
    with engine.begin() as conn:
        conn.execute(query, rows)