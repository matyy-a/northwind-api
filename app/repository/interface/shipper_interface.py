from abc import ABC, abstractmethod
from app.models.sales.shipper_model import Shipper

class ShipperInterface:
    @abstractmethod
    async def get_shipper(self, id: int) -> Shipper | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Shipper]:
        pass

    @abstractmethod
    async def create_shipper(self, shipper_name: str, phone: str) -> Shipper | None:
        pass

    @abstractmethod
    async def update_shipper(self, shipper_id: int, shipper_name: str, phone: str) -> Shipper | None:
        pass

    @abstractmethod
    async def delete_shipper(self, shipper_id: int) -> bool:
        pass


