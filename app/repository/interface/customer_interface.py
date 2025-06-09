from abc import ABC, abstractmethod
from app.models.sales.customer_model import Customer

class CustomerInterface(ABC):
    
    @abstractmethod
    async def get_customer(self, id: int) -> Customer | None:
        pass
    
    @abstractmethod
    async def get_all(self) -> list[Customer]:
        pass

    @abstractmethod
    async def create_customer(self, customer_name: str, contact_name: str, address: str,
                        city: str, postal_code: str, country: str) -> Customer | None:
        pass

    @abstractmethod
    async def update_customer(self, customer_id: int, customer_name: str, contact_name: str,
                        address: str, city: str, postal_code: str, country: str) -> Customer | None:
        pass

    @abstractmethod
    async def delete_customer(self, customer_id: int) -> bool:
        pass