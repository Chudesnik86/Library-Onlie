from pydantic import BaseModel
from typing import Optional


class TokenDTO(BaseModel):
    """DTO для токена"""
    access_token: str
    token_type: str


class TokenDataDTO(BaseModel):
    """DTO для данных токена"""
    username: Optional[str] = None


class UserLoginDTO(BaseModel):
    """DTO для входа пользователя"""
    username: str
    password: str


class UserResponseDTO(BaseModel):
    """DTO для ответа с пользователем"""
    username: str




