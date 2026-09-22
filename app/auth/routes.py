from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError

from app.auth.jwt import create_access_token
from app.config import JWT_EXPIRES_MINUTES
from app.auth.dependencies import get_token_payload
from app.repositories.alunos_repository import (
    criar_aluno,
    buscar_aluno_por_email,
    verificar_senha,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


class RegisterRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class AlunoOut(BaseModel):
    id_aluno: str
    nome: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    aluno: AlunoOut


def _gerar_token_response(aluno: dict) -> dict:
    expires = timedelta(minutes=JWT_EXPIRES_MINUTES)
    token = create_access_token(data={"sub": str(aluno["id_aluno"])}, expires_delta=expires)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRES_MINUTES * 60,
        "aluno": {
            "id_aluno": str(aluno["id_aluno"]),
            "nome": aluno["nome"],
            "email": aluno["email"],
        },
    }


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest):
    if len(data.senha) < 6:
        raise HTTPException(status_code=400, detail="A senha precisa ter no mínimo 6 caracteres.")

    try:
        aluno = criar_aluno(data.nome, data.email, data.senha)
    except IntegrityError as e:
        if "email" in str(e.orig).lower():
            raise HTTPException(status_code=400, detail="Esse email já está cadastrado.")
        raise HTTPException(status_code=500, detail="Erro ao criar conta. Tente novamente.")

    return _gerar_token_response(aluno)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    aluno = buscar_aluno_por_email(data.email)

    if not aluno or not verificar_senha(data.senha, aluno["senha_hash"]):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos.")

    return _gerar_token_response(aluno)


@router.get("/status")
def auth_status():
    return {"status": "auth route ativa"}


@router.get("/debug-token")
def debug_token(payload: dict = Depends(get_token_payload)):
    return {"token_payload": payload}