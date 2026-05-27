from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.jwt import decode_access_token

bearer_scheme = HTTPBearer()


def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    token = credentials.credentials or ""
    # Aceita valores com ou sem o prefixo 'Bearer '
    if token.lower().startswith("bearer "):
        token = token.split(" ", 1)[1]
    payload = decode_access_token(token)
    return payload


def get_current_user_id(token_payload: dict = Depends(get_token_payload)) -> str:
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido ou sem informação de usuário")
    return user_id
