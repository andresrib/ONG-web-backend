import configparser
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." / ".."))

parser = configparser.ConfigParser()
config_file = Path("FastAPI/database/config.ini")
parser.read(config_file)

user = parser.get("database", "user")
passwd = parser.get("database", "pass")
db_name = parser.get("database", "db")
host = parser.get("database", "host")
