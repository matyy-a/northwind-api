from fastapi import HTTPException
from datetime import timedelta
from app.repository.user_repository import UserRepository
from app.services.auth.security_service import SecurityService
from app.services.auth.token_service import TokenService
from app.models.auth.user_model import User
from app.schemas.auth.auth_schema import Token
from app.utils.config import settings

class AuthService:
    def __init__(self, user_repository: UserRepository, security_service: SecurityService, token_service: TokenService):
        self.user_repository = user_repository
        self.security_service = security_service
        self.token_service = token_service
    
    async def authenticate(self, username: str, password: str) -> User | bool:
        user = await self.user_repository.get_user_by_username_or_email(username)
        if not user:
            return False
        if not self.security_service.verify_password(password, user.hashed_password):
            return False
        return user
    
    async def login(self, username: str, password: str) -> dict | None:
        user = await self.authenticate(username, password)
        if not user:
            return None
        
        access_token = await self.token_service.create_access_token(
            data={"sub": user.username}, expire_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        return Token(access_token=access_token, token_type="bearer")

    async def logout(self, token: str):
        return await self.token_service.invalidate_token(token)
    
    async def get_current_user_from_token(self, token: str) -> User | None:
        try:
            payload = await self.token_service.decode_access_token(token)
            username: str = payload.get("sub")
            
            if not username:
                return None
            
            user = await self.user_repository.get_user_by_username_or_email(username)
            return user
            
        except HTTPException:
            return None
    

    




