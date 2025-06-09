from app.repository.order_repository import OrderRepository
from app.repository.customer_repository import CustomerRepository
from app.repository.employee_repository import EmployeeRepository
from app.repository.shipper_repository import ShipperRepository
from app.models.sales.order_model import Order
from datetime import datetime

class OrderService:
    def __init__(self, order_repository: OrderRepository, customer_repository: CustomerRepository, 
                 employee_repository: EmployeeRepository, shipper_repository: ShipperRepository):
        self.order_repository = order_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository
        self.shipper_repository = shipper_repository

    async def get_order(self, order_id: int) -> Order | None:
        return await self.order_repository.get_order(order_id)
    
    async def get_all_orders(self) -> list[Order] | None:
        return await self.order_repository.get_all()
    
    async def create_order(self, customer_id: int, employee_id: int, 
                          order_date: datetime, shipper_id: int) -> Order | None:
        if not await self.customer_repository.get_customer(customer_id):
            return None
        
        if not await self.employee_repository.get_employee(employee_id):
            return None
        
        if not await self.shipper_repository.get_shipper(shipper_id):
            return None
        
        return await self.order_repository.create_order(customer_id, employee_id, order_date, shipper_id)
    
    async def update_order(self, order_id: int, customer_id: int, employee_id: int,
                          order_date: datetime, shipper_id: int) -> Order | None:
        if not await self.customer_repository.get_customer(customer_id):
            return None
        
        if not await self.employee_repository.get_employee(employee_id):
            return None
        
        if not await self.shipper_repository.get_shipper(shipper_id):
            return None
        
        return await self.order_repository.update_order(order_id, customer_id, employee_id, 
                                                       order_date, shipper_id)
    
    async def delete_order(self, order_id: int) -> bool:
        return await self.order_repository.delete_order(order_id)