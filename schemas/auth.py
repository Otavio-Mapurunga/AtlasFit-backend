from pydantic import BaseModel, EmailStr
from typing import Literal, Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    goal: Optional[Literal["hipertrofia", "emagrecimento", "forca", "resistencia"]] = None
    experience_level: Optional[Literal["iniciante", "intermediario", "avancado"]] = None
    training_frequency: Optional[int] = None
    limitations: Optional[list[str]] = None
    equipment: Optional[list[str]] = None
    preferences: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ErrorResponse(BaseModel):
    detail: str
