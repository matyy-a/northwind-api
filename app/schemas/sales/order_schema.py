from pydantic import BaseModel
from datetime import datetime

class OrderCreateSchema(BaseModel):
    CustomerID: int
    EmployeeID: int
    OrderDate: datetime
    ShipperID: int

class OrderOutSchema(BaseModel):
    OrderID: int
    CustomerID: int
    EmployeeID: int
    OrderDate: datetime
    ShipperID: int

class OrderDetailCreateSchema(BaseModel):
    OrderID: int
    ProductID: int
    Quantity: int

class OrderDetailOutSchema(BaseModel):
    OrderDetailID: int
    OrderID: int
    ProductID: int
    Quantity: int