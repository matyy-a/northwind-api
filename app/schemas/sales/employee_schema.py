from pydantic import BaseModel
from datetime import date

class EmployeeCreateSchema(BaseModel):
    LastName: str
    FirstName: str
    BirthDate: date
    Photo: str
    Notes: str

class EmployeeOutSchema(BaseModel):
    EmployeeID: int
    LastName: str
    FirstName: str
    BirthDate: date
    Photo: str
    Notes: str