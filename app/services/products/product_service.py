from app.repository.supplier_repository import SupplierRepository
from app.repository.category_repository import CategoryRepository
from app.repository.product_repository import ProductRepository
from app.models.products.product_model import Product

class ProductService:
    def __init__(self, product_repository: ProductRepository, supplier_repository: SupplierRepository, category_repository: CategoryRepository):
        self.supplier_repository = supplier_repository
        self.category_repository = category_repository
        self.product_repository = product_repository

    async def get_product(self, product_id: int) -> Product | None:
        return await self.product_repository.get_product(product_id)
    
    async def get_all_products(self) -> list[Product] | None:
        return await self.product_repository.get_all()
    
    async def create_product(self, product_name: str, supplier_id: int, category_id: int,
                             unit: str, price: float) -> Product | None:
        if not await self.category_repository.get_category(category_id):
            return None
        
        if not await self.supplier_repository.get_supplier(supplier_id):
            return None
        
        return await self.product_repository.create_product(product_name, supplier_id, category_id, unit, price)
    
    async def update_product(self, product_id: int, product_name: str, supplier_id: int, category_id: int,
                             unit: str, price: float) -> Product | None:
        if not await self.category_repository.get_category(category_id):
            return None
        
        if not await self.supplier_repository.get_supplier(supplier_id):
            return None
        
        return await self.product_repository.update_product(product_id, product_name, supplier_id, category_id,
                                                            unit, price)
    
    async def delete_product(self, product_id: int) -> bool:
        return await self.product_repository.delete_product(product_id)