from uuid import uuid4
from sqlalchemy.orm import Session
import sqlalchemy


import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.user import UserPost
from database.database import engine
from models.user import UserModel
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