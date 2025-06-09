from app.repository.category_repository import CategoryRepository
from app.models.products.category_model import Category

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository=category_repository
    
    async def get_all_categories(self) -> list[Category] | None:
        return await self.category_repository.get_all()

    async def get_category(self, id_category: int) -> Category | None:
        return await self.category_repository.get_category(id_category)
    
    async def update_category(self, id_category: int, name_category: str, description: str) -> Category | None:
        return await self.category_repository.update_category(id_category, name_category, description)
    
    async def delete_category(self, id_category: int) -> bool:
        return await self.category_repository.delete_category(id_category)
    
    async def create_category(self, name_category: str, description: str) -> Category | None:
        return await self.category_repository.create_category(name_category, description)
