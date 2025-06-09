from app.models.auth.user_model import User
from app.repository.user_repository import UserRepository
from app.services.auth.security_service import SecurityService

class UserService:
    def __init__(self, user_repository: UserRepository, security_service: SecurityService):
        self.user_repository = user_repository
        self.security_service = security_service
    
    async def create_user(self, username: str, email: str, password: str) -> User | None:
        hashed_password = self.security_service.hash_password(password)
        new_user = await self.user_repository.create_user(username, email, hashed_password)
        return new_user
    
    async def get_user(self, username_or_email) -> User | None:
        return await self.user_repository.get_user_by_username_or_email(username_or_email)
