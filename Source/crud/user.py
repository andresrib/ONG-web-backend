from uuid import uuid4
from sqlalchemy.orm import Session
import sqlalchemy


import os
import sys
from pathlib import Path

from sqlalchemy.sql.expression import true
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.user import UserPost
from database.database import engine
from crud.login import get_password_hash
from models.user import UserModel
from models.ong import OngModel
import logging


def insert_user(db: Session, user: UserPost):
    status = False
    try:
        user_id = uuid4()
        user_id = str(user_id).replace("-", "")
        db_user = UserModel(
            **user.dict(), user_id=user_id, ong_id="")
        
        db.add(db_user)
        #db.execute("INSERT INTO user(user_id, name, password, email, cellphone) VALUES('" + str(user_id) + "', '" + user.name + "', '" + user.password + "', '" + user.email + "', '" + user.cellphone + "')")
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
        data = {"ErrorInsertingData"}
    finally:
        return {
            "status": status,
            "user_id": user_id
        }

def update_user(db: Session, id: str, user: UserPost):
    try:
        password = get_password_hash(user.password)
        db.query(UserModel).filter(UserModel.user_id==id).update({"name": user.name, "email": user.email, "cellphone": user.cellphone, "password": password})
        db.commit()
        status = True
    except:
        status = False
    return {"status": status}

def retrieve_users(db: Session, id: str):
    try:
        user = db.query(UserModel, OngModel).filter(UserModel.ong_id == OngModel.ong_id).filter_by(user_id=id).first()
        status = True
    except:
        logging.exception("teste")
        user = {}
        status = False
    return {"user": user, "status": status}
        