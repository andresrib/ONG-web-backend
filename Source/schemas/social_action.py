from pydantic import BaseModel
from typing import Optional

class SocialActionPost(BaseModel):
    name: str
    goal: float
    description: str
    current_money: float
    ong_id: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "ong",
                "goal": 1000,
                "description": "descricao",
                "current_money": 3,
                "ong_id": "uuid"
            }
        }