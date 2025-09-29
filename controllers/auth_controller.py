from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services import AuthService
from dto import UserLoginDTO, TokenDTO, UserResponseDTO
from database import get_db
from services.auth_service import verify_token

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """Получить сервис аутентификации"""
    return AuthService(db)


@router.post("/login", response_model=TokenDTO)
async def login(
    user_credentials: UserLoginDTO,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Войти в систему"""
    token = auth_service.login(user_credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/me", response_model=UserResponseDTO)
async def get_current_user(
    current_user: str = Depends(verify_token)
):
    """Получить текущего пользователя"""
    return UserResponseDTO(username=current_user)
