from datetime import timedelta
from typing import Optional
from auth import authenticate_user, create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
from dto import UserLoginDTO, TokenDTO, UserResponseDTO


class AuthService:
    """Сервис для аутентификации"""
    
    def login(self, user_credentials: UserLoginDTO) -> Optional[TokenDTO]:
        """Войти в систему"""
        user = authenticate_user(user_credentials.username, user_credentials.password)
        if not user:
            return None
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"]}, 
            expires_delta=access_token_expires
        )
        
        return TokenDTO(
            access_token=access_token,
            token_type="bearer"
        )
    
    def get_current_user(self, token: str) -> Optional[UserResponseDTO]:
        """Получить текущего пользователя по токену"""
        username = verify_token(token)
        if not username:
            return None
        
        return UserResponseDTO(username=username)
    
    def verify_token(self, token: str) -> Optional[str]:
        """Проверить токен"""
        return verify_token(token)




