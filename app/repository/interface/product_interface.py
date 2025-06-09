from abc import ABC, abstractmethod
from app.models.products.product_model import Product

class ProductInterface:
    
    @abstractmethod
    async def get_product(self, product_id: int) -> Product | None:
        pass

    @abstractmethod
    async def get_all(self) -> Product | None:
        pass

    @abstractmethod
    async def create_product(self, product_id: int, product_name: str, supplier_id: int, category_id: int,
                         unit: str, price: float):
        pass

    @abstractmethod
    async def update_product(self, product_id: int, product_name: str, supplier_id: int, category_id: int,
                         unit: str, price: float) -> Product | None:
        pass

    @abstractmethod
    async def delete_product(self, product_id: int) -> bool:
        pass