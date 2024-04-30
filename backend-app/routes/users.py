from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import redis
from app.models import User
from app.database import get_db
from app.schema import UserCreate

user_router = APIRouter(prefix="/users")
redis_client = redis.Redis(host='localhost', port=6379, db=0)


@user_router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

