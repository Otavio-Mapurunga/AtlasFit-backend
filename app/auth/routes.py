from datetime import timedelta

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.jwt import create_access_token
from app.config import JWT_EXPIRES_MINUTES
from app.auth.dependencies import get_token_payload

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    user_id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    expires = timedelta(minutes=JWT_EXPIRES_MINUTES)
    token = create_access_token(data={"sub": data.user_id}, expires_delta=expires)
    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_EXPIRES_MINUTES * 60}


@router.get("/status")
def auth_status():
    return {"status": "auth route ativa"}


@router.get("/debug-token")
def debug_token(payload: dict = Depends(get_token_payload)):
    # Endpoint de debug para desenvolvimento — retorna o payload do token
    return {"token_payload": payload}
