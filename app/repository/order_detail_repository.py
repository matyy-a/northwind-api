from app.repository.interface.order_detail_interface import OrderDetailInterface
from app.models.sales.order_detail import OrderDetail
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

class OrderDetailRepository(OrderDetailInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_order_detail(self, order_detail_id: int) -> OrderDetail | None:
        result = await self.db_session.execute(
            select(OrderDetail).where(OrderDetail.OrderDetailID == order_detail_id)
        )
        return result.scalar_one_or_none()
    
    async def get_details_by_order_id(self, order_id: int) -> list[OrderDetail] | None:
        result = await self.db_session.execute(
            select(OrderDetail).where(OrderDetail.OrderID == order_id)
        )
        return result.scalars().all()
    
    async def get_all(self) -> list[OrderDetail] | None:
        result = await self.db_session.execute(select(OrderDetail))
        return result.scalars().all()
    
    async def create_order_detail(self, order_id: int, product_id: int, 
                                 quantity: int) -> OrderDetail | None:
        
        new_order_detail = OrderDetail(
            OrderID=order_id,
            ProductID=product_id,
            Quantity=quantity
        )

        try:
            self.db_session.add(new_order_detail)
            await self.db_session.commit()
            await self.db_session.refresh(new_order_detail)
            return new_order_detail
        except IntegrityError:
            await self.db_session.rollback()
            return None

    async def update_order_detail(self, order_detail_id: int, order_id: int, 
                                 product_id: int, quantity: int) -> OrderDetail | None:
               
        result = await self.db_session.execute(
            select(OrderDetail).where(OrderDetail.OrderDetailID == order_detail_id)
        )

        order_detail = result.scalar_one_or_none()

        if not order_detail:
            return None
        
        order_detail.OrderID = order_id
        order_detail.ProductID = product_id
        order_detail.Quantity = quantity

        try:
            await self.db_session.commit()
            await self.db_session.refresh(order_detail)
            return order_detail
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_order_detail(self, order_detail_id: int) -> bool:
        result = await self.db_session.execute(
            select(OrderDetail).where(OrderDetail.OrderDetailID == order_detail_id)
        )
        order_detail = result.scalar_one_or_none()

        if not order_detail:
            return False

        try:
            await self.db_session.delete(order_detail)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False