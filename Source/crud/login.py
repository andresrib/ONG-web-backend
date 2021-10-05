from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status as fastapi_status,
)
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from database.database import get_db, engine

import logging

####
# constants
# chave secreta da nossa aplicação que pode ser alterada de tempos em tempos
SECRET_KEY = "0a54f19e893f41f699d4a264e32300cc"
# tipo da cripto a ser utilizada
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 4320
###########

### Define algumas classes q nao sei mexer nelas ainda


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    hashed_password: Optional[str]


###############
# crud part
async def retrieve_usernames(db: Session, username):
    """Função chamada pela rota post login, retorna o email de um user"""
    try:
        users = engine.execute(
            "SELECT email FROM user WHERE email = '" + username + "'"
        )
        return users.fetchone().email
    except Exception:
        logging.exception("ErrorRetrieveUsernames")
        return {}


async def retrieve_password(db: Session, username):
    """Função chamada pela rota post login, retorna a senha de um user"""
    try:
        users = engine.execute(
            "SELECT password FROM user WHERE email = '" + username + "'"
        )
        return users.fetchall()[0].password
    except Exception:
        logging.exception("ErrorRetrievePassword")
        return {}


async def get_user_login(username: str, db: Session = Depends(get_db)):
    """tras os dados de login do banco e verifica se o usuario existe"""
    users = await retrieve_usernames(db, username)
    if username in users:
        return users


##############

# objetos criados para a estrutura de autenticassao

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
login_router = APIRouter()

##############
# UTILS
def verify_password(plain_password, hashed_password):
    """verifica se a senha inserida no login é válida para o usuario"""
    if pwd_context.verify(plain_password, hashed_password):
        # if plain_password == hashed_password:
        return True
    else:
        return False


####deve ser colocoado no endpoint POST USER
### criar novo endpoitn para resetar a senha e atualizar
def get_password_hash(password):
    """criptografa a senha"""
    return pwd_context.hash(password)


# chamado pela rota de autentication
async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    """verifica se o usuario é valido"""
    user = await retrieve_usernames(db, username)
    print(user)
    if not user:
        return False
    if not verify_password(password, await retrieve_password(db, username)):
        return False
    return user


# codifica o token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """cria um token de acesso para permitir
    o uso de funções restritas por login"""

    # DATA contem o usuario  q esta logando
    to_encode = data.copy()
    # codifica o horario atual e etc para criar um token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # encoded_jwt sao os dados de usuario e expire time juntos e  encriptados
    return encoded_jwt


# DEcodifica o token
# verifica qual eh o usuario q esta logando - serve para tratar casos onde determinado
# usuario n tem acesso a deerminado recurso
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    """verifica se o usuario logado é valido"""
    # caso o token seja invalido explode o except abaixo
    credentials_exception = HTTPException(
        status_code=fastapi_status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decodifica o token - faz o oposto da function create_acess_token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_login(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def retrieve_login_information(db, user):
    try:
        query_get_login_information = (
            "SELECT * FROM user WHERE email = '" + user + "'"
        )
        data = engine.execute(query_get_login_information).fetchone()
        #name = data.name
        #telephone = data.telephone
    except:
        data = False
        #name = ""
        #telephone = ""
        logging.exception("ErrorGettingLoginData")
    finally:
      return data
#async def validate_permission(token, list_accepted):
#    _, user_role = await get_current_user_from_token(token=token)
#    if not user_role in list_accepted:
#        return False
#    else:
#        return True


####################################
# a decidir
#async def get_current_active_user(
#    current_user: User = Depends(get_current_user_from_token),
#):
#    """verifica se o usuario está logado e restringe usuarios não logados"""
#    # if current_user.disabled:
#    #    raise HTTPException(status_code=400, detail="Inactive user")
#    return current_user
