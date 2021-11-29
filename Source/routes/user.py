from fastapi import FastAPI, APIRouter, Depends, Response, status as fastAPI_status
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.user import UserPost, UserPut
from database.database import get_db
from crud.user import insert_user, retrieve_users, update_user
from crud.login import get_password_hash, oauth2_scheme, get_current_user_from_token, retrieve_login_information

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
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    return update_user(db, id, user)

@user_router.get("/user")
async def get_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = await get_current_user_from_token(token)
    id = await retrieve_login_information(db, user)
    return retrieve_users(db, id.user_id)