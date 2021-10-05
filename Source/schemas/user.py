from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPost(BaseModel):
    email: EmailStr
    name: str
    password: str
    cellphone: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "andre@gmail.com",
                "name": "andre",
                "password": "ong123",
                "cellphone": "32485284"
            }
        }

class Login(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "andre@gmail.com",
                "password": "ong123",
            }
        }
    