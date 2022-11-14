import os
import jwt

from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from db.db_setup import get_db
from db.models.user import User

path = Path('.env').absolute()
load_dotenv(path)

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 60
bearer_scheme = OAuth2PasswordBearer(tokenUrl='signin')


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def validate_token(
    token: str = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid token',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name = payload.get('name')

        if name is None:
            raise invalid_token_exception

    except jwt.PyJWTError:
        raise invalid_token_exception

    user = db.query(User).filter(User.name == name).first()

    if user is None:
        raise invalid_token_exception

    return user


def hash_password(password: str) -> str:
    return password + 'fake_hash'
