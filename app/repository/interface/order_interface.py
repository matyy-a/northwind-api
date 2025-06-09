from abc import ABC, abstractmethod
from app.models.sales.order_model import Order
from datetime import datetime

class OrderInterface(ABC):
    
    @abstractmethod
    async def get_order(self, order_id: int) -> Order | None:
        pass
    
    @abstractmethod
    async def get_all(self) -> list[Order] | None:
        pass
    
    @abstractmethod
    async def create_order(self, customer_id: int, employee_id: int, 
                          order_date: datetime, shipper_id: int) -> Order | None:
        pass
    
    @abstractmethod
    async def update_order(self, order_id: int, customer_id: int, employee_id: int,
                          order_date: datetime, shipper_id: int) -> Order | None:
        pass
    
    @abstractmethod
    async def delete_order(self, order_id: int) -> bool:
        pass