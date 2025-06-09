from abc import ABC, abstractmethod
from app.models.sales.order_detail import OrderDetail

class OrderDetailInterface(ABC):
    
    @abstractmethod
    async def get_order_detail(self, order_detail_id: int) -> OrderDetail | None:
        pass
    
    @abstractmethod
    async def get_details_by_order_id(self, order_id: int) -> list[OrderDetail] | None:
        pass
    
    @abstractmethod
    async def get_all(self) -> list[OrderDetail] | None:
        pass
    
    @abstractmethod
    async def create_order_detail(self, order_id: int, product_id: int, 
                                 quantity: int) -> OrderDetail | None:
        pass
    
    @abstractmethod
    async def update_order_detail(self, order_detail_id: int, order_id: int, 
                                 product_id: int, quantity: int) -> OrderDetail | None:
        pass
    
    @abstractmethod
    async def delete_order_detail(self, order_detail_id: int) -> bool:
        pass