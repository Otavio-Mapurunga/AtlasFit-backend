from fastapi import APIRouter, HTTPException, status

from backend.schemas.auth import LoginRequest, LoginResponse, UserResponse
from backend.services.supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login do usuário",
    description="Autentica o usuário com email e senha via Supabase Auth e retorna o token de acesso.",
    responses={
        200: {"description": "Login realizado com sucesso"},
        401: {"description": "Email ou senha inválidos"},
        422: {"description": "Dados de entrada inválidos"},
        500: {"description": "Erro interno no servidor"},
    },
)
async def login(credentials: LoginRequest) -> LoginResponse:
    """
    Realiza o login do usuário.

    - **email**: Email cadastrado do usuário
    - **password**: Senha do usuário

    Retorna um `access_token` JWT e os dados do perfil do usuário.
    """
    try:
        # Autenticação via Supabase Auth
        auth_response = supabase.auth.sign_in_with_password(
            {"email": credentials.email, "password": credentials.password}
        )
    except Exception as e:
        error_msg = str(e).lower()
        if "invalid" in error_msg or "credentials" in error_msg or "password" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha inválidos",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao conectar com o serviço de autenticação",
        ) from e

    if not auth_response.session or not auth_response.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
        )

    auth_user = auth_response.user
    access_token = auth_response.session.access_token

    # Buscar dados do perfil na tabela 'profiles' do Supabase
    try:
        profile_response = (
            supabase.table("profiles")
            .select("*")
            .eq("id", auth_user.id)
            .single()
            .execute()
        )
        profile = profile_response.data or {}
    except Exception:
        # Se não houver tabela de perfis, usa só os dados do Auth
        profile = {}

    user = UserResponse(
        id=str(auth_user.id),
        name=profile.get("name") or (auth_user.user_metadata or {}).get("name", ""),
        email=auth_user.email or "",
        height=profile.get("height"),
        weight=profile.get("weight"),
        age=profile.get("age"),
        goal=profile.get("goal"),
        experience_level=profile.get("experience_level"),
        training_frequency=profile.get("training_frequency"),
        limitations=profile.get("limitations"),
        equipment=profile.get("equipment"),
        preferences=profile.get("preferences"),
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )
