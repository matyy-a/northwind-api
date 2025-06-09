from app.repository.interface.product_interface import ProductInterface
from app.models.products.product_model import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

class ProductRepository(ProductInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_product(self, product_id: int) -> Product | None:
        result = await self.db_session.execute(
            select(Product).where(Product.ProductID == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> Product | None:
        result = await self.db_session.execute(select(Product))
        return result.scalars().all()
    
    async def create_product(self, product_name: str, supplier_id: int, category_id: int,
                             unit: str, price: float):
        
        new_product = Product(
            ProductName=product_name,
            SupplierID=supplier_id,
            CategoryID=category_id,
            Unit=unit,
            Price=price
        )

        try:
            self.db_session.add(new_product)
            await self.db_session.commit()
            await self.db_session.refresh(new_product)
            return new_product
        except IntegrityError:
            await self.db_session.rollback()
            return None


    async def update_product(self, product_id: int, product_name: str, supplier_id: int, category_id: int,
                             unit: str, price: float) -> Product | None:
               
        result = await self.db_session.execute(
            select(Product).where(Product.ProductID == product_id)
        )

        product = result.scalar_one_or_none()

        if not product:
            return None
        
        product.ProductName=product_name
        product.SupplierID=supplier_id
        product.CategoryID=category_id
        product.Unit=unit
        product.Price=price

        try:
            await self.db_session.commit()
            await self.db_session.refresh(product)
            return product
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_product(self, product_id: int) -> bool:
        result = await self.db_session.execute(
            select(Product).where(Product.ProductID == product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            return False

        try:
            await self.db_session.delete(product)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False
