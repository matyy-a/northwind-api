from app.repository.interface.category_interface import CategoryInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.products.category_model import Category

class CategoryRepository(CategoryInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_category(self, id: int) -> Category | None:
        result = await self.db_session.execute(
            select(Category).where(Category.CategoryID == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Category]:
        result = await self.db_session.execute(select(Category))
        return result.scalars().all()

    async def create_category(self, categoryname: str, description: str) -> Category | None:
        new_category = Category(
            CategoryName=categoryname,
            Description=description,
        )
        try:
            self.db_session.add(new_category)
            await self.db_session.commit()
            await self.db_session.refresh(new_category)
            return new_category
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def update_category(self, category_id: int, categoryname: str, description: str) -> Category | None:
        result = await self.db_session.execute(
            select(Category).where(Category.CategoryID == category_id)
        )
        category = result.scalar_one_or_none()

        if not category:
            return None

        category.CategoryName = categoryname
        category.Description = description

        try:
            await self.db_session.commit()
            await self.db_session.refresh(category)
            return category
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_category(self, category_id: int) -> bool:
        result = await self.db_session.execute(
            select(Category).where(Category.CategoryID == category_id)
        )
        category = result.scalar_one_or_none()

        if not category:
            return False

        try:
            await self.db_session.delete(category)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False


    
