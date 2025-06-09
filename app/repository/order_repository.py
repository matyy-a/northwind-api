from app.repository.interface.order_interface import OrderInterface
from app.models.sales.order_model import Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from datetime import datetime

class OrderRepository(OrderInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_order(self, order_id: int) -> Order | None:
        result = await self.db_session.execute(
            select(Order).where(Order.OrderID == order_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> list[Order] | None:
        result = await self.db_session.execute(select(Order))
        return result.scalars().all()
    
    async def create_order(self, customer_id: int, employee_id: int, 
                          order_date: datetime, shipper_id: int) -> Order | None:
        
        new_order = Order(
            CustomerID=customer_id,
            EmployeeID=employee_id,
            OrderDate=order_date,
            ShipperID=shipper_id
        )

        try:
            self.db_session.add(new_order)
            await self.db_session.commit()
            await self.db_session.refresh(new_order)
            return new_order
        except IntegrityError:
            await self.db_session.rollback()
            return None

    async def update_order(self, order_id: int, customer_id: int, employee_id: int,
                          order_date: datetime, shipper_id: int) -> Order | None:
               
        result = await self.db_session.execute(
            select(Order).where(Order.OrderID == order_id)
        )

        order = result.scalar_one_or_none()

        if not order:
            return None
        
        order.CustomerID = customer_id
        order.EmployeeID = employee_id
        order.OrderDate = order_date
        order.ShipperID = shipper_id

        try:
            await self.db_session.commit()
            await self.db_session.refresh(order)
            return order
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_order(self, order_id: int) -> bool:
        result = await self.db_session.execute(
            select(Order).where(Order.OrderID == order_id)
        )
        order = result.scalar_one_or_none()

        if not order:
            return False

        try:
            await self.db_session.delete(order)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False