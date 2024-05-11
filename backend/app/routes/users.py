from fastapi import APIRouter
from app import crud
from app.schema import UserCreate

user_router = APIRouter(prefix="/users")


@user_router.post("/")
def create_user(user: UserCreate):
    return crud.create_user(user=user)
