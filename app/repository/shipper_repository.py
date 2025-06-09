from app.repository.interface.shipper_interface import ShipperInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.sales.shipper_model import Shipper

class ShipperRepository(ShipperInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_shipper(self, id: int) -> Shipper | None:
        result = await self.db_session.execute(
            select(Shipper).where(Shipper.ShipperID == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Shipper]:
        result = await self.db_session.execute(select(Shipper))
        return result.scalars().all()

    async def create_shipper(self, shipper_name: str, phone: str) -> Shipper | None:
        new_shipper = Shipper(
            ShipperName=shipper_name,
            Phone=phone
        )
        try:
            self.db_session.add(new_shipper)
            await self.db_session.commit()
            await self.db_session.refresh(new_shipper)
            return new_shipper
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def update_shipper(self, shipper_id: int, shipper_name: str, phone: str) -> Shipper | None:
        result = await self.db_session.execute(
            select(Shipper).where(Shipper.ShipperID == shipper_id)
        )
        shipper = result.scalar_one_or_none()

        if not shipper:
            return None

        shipper.ShipperName = shipper_name
        shipper.Phone = phone

        try:
            await self.db_session.commit()
            await self.db_session.refresh(shipper)
            return shipper
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_shipper(self, shipper_id: int) -> bool:
        result = await self.db_session.execute(
            select(Shipper).where(Shipper.ShipperID == shipper_id)
        )
        shipper = result.scalar_one_or_none()

        if not shipper:
            return False

        try:
            await self.db_session.delete(shipper)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False