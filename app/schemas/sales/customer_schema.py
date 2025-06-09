from pydantic import BaseModel

class CustomerCreateSchema(BaseModel):
    CustomerName: str
    ContactName: str
    Address: str
    City: str
    PostalCode: str
    Country: str

class CustomerOutSchema(BaseModel):
    CustomerID: int
    CustomerName: str
    ContactName: str
    Address: str
    City: str
    PostalCode: str
    Country: str