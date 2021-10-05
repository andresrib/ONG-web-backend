from sqlalchemy import create_engine
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." / ".."))


#sqlite_filepath = os.path.dirname(os.path.abspath("database/items.db"))

sqlite_filepath = Path("database/items.db")


engine = create_engine(f"sqlite:///{sqlite_filepath}?check_same_thread=False")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()