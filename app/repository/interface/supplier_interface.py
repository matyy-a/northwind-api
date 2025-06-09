from abc import ABC, abstractmethod
from app.models.products.supplier_model import Supplier

class SupplierInterface(ABC):
    
    @abstractmethod
    async def get_supplier(self, id: int) -> Supplier | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Supplier]:
        pass

    @abstractmethod
    async def create_supplier(self, supplier_name: str, contact_name: str, address: str, 
                        city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        pass

    @abstractmethod
    async def update_supplier(self, supplier_id: int, supplier_name: str, contact_name: str, 
                        address: str, city: str, postal_code: str, country: str, phone: str) -> Supplier | None:
        pass

    @abstractmethod
    async def delete_supplier(self, supplier_id: int) -> bool:
        pass