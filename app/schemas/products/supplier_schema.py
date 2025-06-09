from pydantic import BaseModel

class SupplierCreateSchema(BaseModel):
    SupplierName: str
    ContactName: str
    Address: str
    City: str
    PostalCode: str
    Country: str
    Phone: str

class SupplierOutSchema(BaseModel):
    SupplierID: int
    SupplierName: str
    ContactName: str
    Address: str
    City: str
    PostalCode: str
    Country: str
    Phone: str