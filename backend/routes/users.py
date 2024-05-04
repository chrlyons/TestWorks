from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import crud
from backend.database import get_db
from backend.schema import UserCreate

user_router = APIRouter(prefix="/users")


@user_router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)
