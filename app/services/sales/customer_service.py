from app.repository.customer_repository import CustomerRepository
from app.models.sales.customer_model import Customer

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.customer_repository = customer_repository
    
    async def get_all_customers(self) -> list[Customer]:
        return await self.customer_repository.get_all()

    async def get_customer(self, id_customer: int) -> Customer | None:
        return await self.customer_repository.get_customer(id_customer)
    
    async def update_customer(self, id_customer: int, customer_name: str, contact_name: str,
                            address: str, city: str, postal_code: str, country: str) -> Customer | None:
        return await self.customer_repository.update_customer(id_customer, customer_name, contact_name,
                                                            address, city, postal_code, country)
    
    async def delete_customer(self, id_customer: int) -> bool:
        return await self.customer_repository.delete_customer(id_customer)
    
    async def create_customer(self, customer_name: str, contact_name: str, address: str,
                            city: str, postal_code: str, country: str) -> Customer | None:
        return await self.customer_repository.create_customer(customer_name, contact_name, address,
                                                            city, postal_code, country)