from pydantic import BaseModel

class ShipperCreateSchema(BaseModel):
    ShipperName: str
    Phone: str

class ShipperOutSchema(BaseModel):
    ShipperID: int
    ShipperName: str
    Phone: str