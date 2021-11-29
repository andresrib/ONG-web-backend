from fastapi import FastAPI, APIRouter, Depends, Response, status as fastAPI_status
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from database.database import get_db
from schemas.social_action import SocialActionPost
from crud.social_action import *
from crud.login import oauth2_scheme, get_current_user_from_token, retrieve_login_information

action_router = APIRouter()

@action_router.post("/action")
async def create_action(
    response: Response,
    action: SocialActionPost,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    email = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, email)
    return insert_social_action(db, action, user.user_id)

@action_router.get("/action/{id}")
async def get_action(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return retrieve_social_action(db, id)

@action_router.get("/ong/action/{id}")
async def get_action(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return retrieve_social_action_by_ong(db, id)

@action_router.put("/action/{id}")
async def put_action(
    action: SocialActionPost,
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
): 
    return update_social_action(db, action, id)

@action_router.delete("/action")
async def dlt_action(
    id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return delete_social_action(db, id)
