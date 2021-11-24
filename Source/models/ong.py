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


class OngModel(Base):
    __tablename__ = "ong"

    ong_id = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    city = Column(TEXT)
    state = Column(TEXT)
    phone = Column(TEXT)