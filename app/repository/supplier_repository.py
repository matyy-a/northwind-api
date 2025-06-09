from app.repository.interface.supplier_interface import SupplierInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.products.supplier_model import Supplier

class SupplierRepository(SupplierInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_supplier(self, id: int) -> Supplier | None:
        result = await self.db_session.execute(
            select(Supplier).where(Supplier.SupplierID == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Supplier]:
        result = await self.db_session.execute(select(Supplier))
        return result.scalars().all()

    async def create_supplier(self, supplier_name: str, contact_name: str, address: str, 
                            city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        new_supplier = Supplier(
            SupplierName=supplier_name,
            ContactName=contact_name,
            Address=address,
            City=city,
            PostalCode=postal_code,
            Country=country,
            Phone=phone
        )
        try:
            self.db_session.add(new_supplier)
            await self.db_session.commit()
            await self.db_session.refresh(new_supplier)
            return new_supplier
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def update_supplier(self, supplier_id: int, supplier_name: str, contact_name: str, 
                            address: str, city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        result = await self.db_session.execute(
            select(Supplier).where(Supplier.SupplierID == supplier_id)
        )
        supplier = result.scalar_one_or_none()

        if not supplier:
            return None

        supplier.SupplierName = supplier_name
        supplier.ContactName = contact_name
        supplier.Address = address
        supplier.City = city
        supplier.PostalCode = postal_code
        supplier.Country = country
        supplier.Phone = phone

        try:
            await self.db_session.commit()
            await self.db_session.refresh(supplier)
            return supplier
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_supplier(self, supplier_id: int) -> bool:
        result = await self.db_session.execute(
            select(Supplier).where(Supplier.SupplierID == supplier_id)
        )
        supplier = result.scalar_one_or_none()

        if not supplier:
            return False

        try:
            await self.db_session.delete(supplier)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False