from app.repository.interface.customer_interface import CustomerInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.sales.customer_model import Customer

class CustomerRepository(CustomerInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_customer(self, id: int) -> Customer | None:
        result = await self.db_session.execute(
            select(Customer).where(Customer.CustomerID == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Customer]:
        result = await self.db_session.execute(select(Customer))
        return result.scalars().all()

    async def create_customer(self, customer_name: str, contact_name: str, address: str,
                            city: str, postal_code: str, country: str) -> Customer | None:
        new_customer = Customer(
            CustomerName=customer_name,
            ContactName=contact_name,
            Address=address,
            City=city,
            PostalCode=postal_code,
            Country=country
        )
        try:
            self.db_session.add(new_customer)
            await self.db_session.commit()
            await self.db_session.refresh(new_customer)
            return new_customer
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def update_customer(self, customer_id: int, customer_name: str, contact_name: str,
                            address: str, city: str, postal_code: str, country: str) -> Customer | None:
        result = await self.db_session.execute(
            select(Customer).where(Customer.CustomerID == customer_id)
        )
        customer = result.scalar_one_or_none()

        if not customer:
            return None

        customer.CustomerName = customer_name
        customer.ContactName = contact_name
        customer.Address = address
        customer.City = city
        customer.PostalCode = postal_code
        customer.Country = country

        try:
            await self.db_session.commit()
            await self.db_session.refresh(customer)
            return customer
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_customer(self, customer_id: int) -> bool:
        result = await self.db_session.execute(
            select(Customer).where(Customer.CustomerID == customer_id)
        )
        customer = result.scalar_one_or_none()

        if not customer:
            return False

        try:
            await self.db_session.delete(customer)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False