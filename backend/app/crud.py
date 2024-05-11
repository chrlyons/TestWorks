from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.orm import Session
import redis
from app.models import User
from app.database import get_db
from app.schema import UserCreate
from fastapi import Depends

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt