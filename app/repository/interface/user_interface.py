from abc import ABC, abstractmethod
from app.models.auth.user_model import User

class UserInterface(ABC):
    
    @abstractmethod
    async def get_user_by_username_or_email(self, username_or_email) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, username: str, email: str, hashed_password: str) -> User | None:
        pass

    
