from abc import ABC, abstractmethod
from app.models.products.category_model import Category

class CategoryInterface(ABC):

    @abstractmethod
    async def get_category(self, id: int) -> Category | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Category]:
        pass

    @abstractmethod
    async def create_category(self, categoryname: str, description: str) -> Category | None:
        pass

    @abstractmethod
    async def update_category(self, category_id: int, categoryname: str, description: str) -> Category | None:
        pass

    @abstractmethod
    async def delete_category(self, category_id: int) -> bool:
        pass