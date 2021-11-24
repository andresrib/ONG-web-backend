from pydantic import BaseModel, EmailStr
from typing import Optional

class OngPost(BaseModel):
    name: str
    city: str
    state: str
    phone: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "andre",
                "city": "pira",
                "state": "sao paulo",
                "phone": "43856235"
            }
        }