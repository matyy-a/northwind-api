from app.repository.supplier_repository import SupplierRepository
from app.models.products.supplier_model import Supplier

class SupplierService:
    def __init__(self, supplier_repository: SupplierRepository):
        self.supplier_repository = supplier_repository
    
    async def get_all_suppliers(self) -> list[Supplier]:
        return await self.supplier_repository.get_all()

    async def get_supplier(self, id_supplier: int) -> Supplier | None:
        return await self.supplier_repository.get_supplier(id_supplier)
    
    async def update_supplier(self, id_supplier: int, supplier_name: str, contact_name: str,
                            address: str, city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        return await self.supplier_repository.update_supplier(id_supplier, supplier_name, contact_name,
                                                            address, city, postal_code, country, phone)
    
    async def delete_supplier(self, id_supplier: int) -> bool:
        return await self.supplier_repository.delete_supplier(id_supplier)
    
    async def create_supplier(self, supplier_name: str, contact_name: str, address: str,
                            city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        return await self.supplier_repository.create_supplier(supplier_name, contact_name, address,
                                                            city, postal_code, country, phone)