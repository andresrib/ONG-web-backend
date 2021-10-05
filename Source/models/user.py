from typing import Text
from sqlalchemy import Column
from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.sqlite import (
    TEXT,
    REAL
)

import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))

from database.database import Base


class UserModel(Base):
    __tablename__ = "user"

    user_id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    ong_id = Column(TEXT)
    email = Column(TEXT)
    password = Column(TEXT)
    cellphone = Column(TEXT)