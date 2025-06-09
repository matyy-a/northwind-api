from app.repository.shipper_repository import ShipperRepository
from app.models.sales.shipper_model import Shipper

class ShipperService:
    def __init__(self, shipper_repository: ShipperRepository):
        self.shipper_repository = shipper_repository
    
    async def get_all_shippers(self) -> list[Shipper]:
        return await self.shipper_repository.get_all()

    async def get_shipper(self, id_shipper: int) -> Shipper | None:
        return await self.shipper_repository.get_shipper(id_shipper)
    
    async def update_shipper(self, id_shipper: int, shipper_name: str, phone: str) -> Shipper | None:
        return await self.shipper_repository.update_shipper(id_shipper, shipper_name, phone)
    
    async def delete_shipper(self, id_shipper: int) -> bool:
        return await self.shipper_repository.delete_shipper(id_shipper)
    
    async def create_shipper(self, shipper_name: str, phone: str) -> Shipper | None:
        return await self.shipper_repository.create_shipper(shipper_name, phone)