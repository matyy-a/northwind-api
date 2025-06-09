from app.repository.order_detail_repository import OrderDetailRepository
from app.repository.order_repository import OrderRepository
from app.repository.product_repository import ProductRepository
from app.models.sales.order_detail import OrderDetail

class OrderDetailService:
    def __init__(self, order_detail_repository: OrderDetailRepository, 
                 order_repository: OrderRepository, product_repository: ProductRepository):
        self.order_detail_repository = order_detail_repository
        self.order_repository = order_repository
        self.product_repository = product_repository

    async def get_order_detail(self, order_detail_id: int) -> OrderDetail | None:
        return await self.order_detail_repository.get_order_detail(order_detail_id)
    
    async def get_details_by_order_id(self, order_id: int) -> list[OrderDetail] | None:
        return await self.order_detail_repository.get_details_by_order_id(order_id)
    
    async def get_all_order_details(self) -> list[OrderDetail] | None:
        return await self.order_detail_repository.get_all()
    
    async def create_order_detail(self, order_id: int, product_id: int, 
                                 quantity: int) -> OrderDetail | None:
        if not await self.order_repository.get_order(order_id):
            return None
        
        if not await self.product_repository.get_product(product_id):
            return None
        
        return await self.order_detail_repository.create_order_detail(order_id, product_id, quantity)
    
    async def update_order_detail(self, order_detail_id: int, order_id: int, 
                                 product_id: int, quantity: int) -> OrderDetail | None:
        if not await self.order_repository.get_order(order_id):
            return None
        
        if not await self.product_repository.get_product(product_id):
            return None
        
        return await self.order_detail_repository.update_order_detail(order_detail_id, order_id, 
                                                                     product_id, quantity)
    
    async def delete_order_detail(self, order_detail_id: int) -> bool:
        return await self.order_detail_repository.delete_order_detail(order_detail_id)