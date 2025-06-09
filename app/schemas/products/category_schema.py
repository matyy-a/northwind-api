from pydantic import BaseModel

class CategoryCreateSchema(BaseModel):
    CategoryName: str
    Description: str

class CategoryOutSchema(BaseModel):
    CategoryID: int
    CategoryName: str
    Description: str