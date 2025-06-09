from app.repository.interface.user_interface import UserInterface
from app.models.auth.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from email_validator import EmailNotValidError, validate_email

class UserRepository(UserInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_username_or_email(self, username_or_email) -> User | None:
        try:
            validate_email(username_or_email)
            filter_condition = (User.email == username_or_email)
        except EmailNotValidError:
            filter_condition = (User.username == username_or_email)
        result = await self.db_session.execute(select(User).where(filter_condition))
        return result.scalars().first()

    async def create_user(self, username: str, email: str, hashed_password: str) -> User | None:
        new_user = User(
            username=username, 
            email=email, 
            hashed_password=hashed_password
        )
        try:
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            return new_user
        except IntegrityError:
            await self.db_session.rollback()
            return None
