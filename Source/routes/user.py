from fastapi import FastAPI, APIRouter, Depends, Response, status as fastAPI_status
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.user import UserPost, UserPut
from database.database import get_db
from crud.user import insert_user
from crud.login import get_password_hash, oauth2_scheme

user_router = APIRouter()

@user_router.post("/user")
async def create_user(
    response: Response,
    user: UserPost,
    db: Session = Depends(get_db)
):
    user.password = get_password_hash(user.password)
    return insert_user(db, user) 

@user_router.post("/user/update/{id}")
async def put_user(
    user: UserPut,
    id: str,
    token: str = Depends(oauth2_scheme)
):
    pass