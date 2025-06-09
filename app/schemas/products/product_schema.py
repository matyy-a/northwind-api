from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    ProductName: str
    SupplierID: int
    CategoryID: int
    Unit: str
    Price: float

class ProductOutSchema(BaseModel):
    ProductID: int
    ProductName: str
    SupplierID: int
    CategoryID: int
    Unit: str
    Price: float