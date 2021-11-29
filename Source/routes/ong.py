from fastapi import FastAPI, APIRouter, Depends, Response, status as fastAPI_status
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.ong import OngPost
from database.database import get_db
from crud.ong import insert_ong, retrieve_ong, retrieve_ong_by_user,update_ong, delete_ong
from crud.login import oauth2_scheme, get_current_user_from_token, retrieve_login_information

ong_router = APIRouter()

@ong_router.post("/ong")
async def create_ong(
    response: Response,
    ong: OngPost,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    email = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, email)
    return insert_ong(db, ong, user.user_id)

@ong_router.get("/ong/{id}")
async def get_ong(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if id == "user":
        email = await get_current_user_from_token(token)
        user = await retrieve_login_information(db, email)  
        return retrieve_ong_by_user(db, user.user_id)
    return retrieve_ong(db, id)

@ong_router.post("/ong/update/{id}")
async def put_ong(
    ong: OngPost,
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
): 
    return update_ong(db, ong, id)

@ong_router.delete("/ong")
async def dlt_ong(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return delete_ong(db, id)
