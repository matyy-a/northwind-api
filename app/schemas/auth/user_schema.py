from pydantic import BaseModel, EmailStr


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr