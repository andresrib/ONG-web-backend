from uuid import uuid4
from sqlalchemy.orm import Session
import sqlalchemy


import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.ong import OngPost
from database.database import engine
from models.ong import OngModel
from models.user import UserModel
import logging


def insert_ong(db: Session, ong: OngPost, user_id: str):
    status = False
    try:
        ong_id = uuid4()
        ong_id = str(ong_id).replace("-", "")
        db_ong = OngModel(ong_id=ong_id, name=ong.name, state=ong.state, city=ong.city, phone=ong.phone)
        
        db.add(db_ong)
        db.query(UserModel).filter_by(user_id=user_id).update({"ong_id": ong_id})
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status,
            "ong_id": ong_id
        }

def retrieve_ong(db: Session, id: str or None):
    try:
        if id == "all":
            ong = db.query(OngModel).all()
        else:
            ong = db.query(OngModel).filter_by(ong_id = id).first()
        status = True
    except:
        ong = []
        logging.exception("ErrorGettingData")
        status = False
    return {"ong": ong, "status": status}


def retrieve_ong_by_user(db: Session, id: str):
    try:
        ong_retorno = []
        ong = db.query(OngModel, UserModel).filter(OngModel.ong_id == UserModel.ong_id).filter(UserModel.user_id == id).all()
        for o in ong:
            ong_retorno.append(o.OngModel)
        status = True
    except:
        ong = []
        logging.exception("ErrorGettingData")
        status = False
    return {"ong": ong_retorno, "status": status}

def update_ong(db: Session, ong: OngPost, id: str):
    try:
        db.query(OngModel).filter(OngModel.ong_id==id).update({"name": ong.name, "phone": ong.phone, "city": ong.city, "state": ong.state})
        db.commit()
        status = True
    except:
        logging.exception("ErrorUpdatangData")
        status = False
    return {"status": status}

def delete_ong(db: Session, id:str):
    try:
        db.query(OngModel).filter_by(ong_id=id).delete()
        db.commit()
        status = True
    except:
        logging.exception("ErrorDeleting")
        status = False
    return {"status": status}

