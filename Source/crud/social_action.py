from uuid import uuid4
from sqlalchemy.orm import Session
import sqlalchemy


import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.social_action import SocialActionPost
from database.database import engine
from models.social_action import SocialActionModel
from models.user import UserModel
import logging


def insert_social_action(db: Session, social_action: SocialActionPost):
    status = False
    try:
        social_action_id = uuid4()
        social_action_id = str(social_action_id).replace("-", "")
        db_social_action = SocialActionModel(case_id=social_action_id, **social_action.dict())
        db.add(db_social_action)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status,
            "social_action_id": social_action_id
        }

def retrieve_social_action(db: Session, id: str or None):
    try:
        if id == "all":
            social_action = db.query(SocialActionModel).all()
        else:
            social_action = db.query(SocialActionModel).filter_by(case_id = id).first()
        status = True
    except:
        social_action = []
        logging.exception("ErrorGettingData")
        status = False
    return {"social_action": social_action, "status": status}

def retrieve_social_action_by_ong(db: Session, id: str):
    try:
        ong = db.query(SocialActionModel).filter(SocialActionModel.ong_id == id).all()
        status = True
    except:
        ong = []
        logging.exception("ErrorGettingData")
        status = False
    return {"ong": ong, "status": status}

def update_social_action(db: Session, social_action: SocialActionPost, id: str):
    try:
        db.query(SocialActionModel).filter(SocialActionModel.case_id==id).update({"name": social_action.name, "goal": social_action.goal, "city": social_action.city, "description": social_action.description, "current_money": social_action.current_money, "ong_id": social_action.ong_id})
        db.commit()
        status = True
    except:
        logging.exception("ErrorUpdatangData")
        status = False
    return {"status": status}

def delete_social_action(db: Session, id:str):
    try:
        db.query(SocialActionModel).filter_by(case_id=id).delete()
        db.commit()
        status = True
    except:
        logging.exception("ErrorDeleting")
        status = False
    return {"status": status}