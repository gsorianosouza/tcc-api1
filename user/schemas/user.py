from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
    
class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"    
    
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.user

class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes = True
