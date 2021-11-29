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

from sqlalchemy.sql.type_api import INTEGERTYPE
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))

from database.database import Base


class SocialActionModel(Base):
    __tablename__ = "social_action"

    case_id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    goal = Column(REAL)
    description = Column(TEXT)
    current_money = Column(REAL)
    ong_id = Column(TEXT)