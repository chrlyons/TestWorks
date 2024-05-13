import json
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.crud import (
    create_access_token,
    create_user,
    get_user_by_username,
    redis_client,
    check_user_token_expiration,
    generate_user_info,
    remove_redis_user,
)
from app.schema import UserCreate
import re
from datetime import datetime, timezone

login_router = APIRouter(prefix="/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@login_router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # Password cannot be 'password'
    if password == "password":
        raise HTTPException(status_code=400, detail="Password cannot be 'password'")

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", username):
        raise HTTPException(status_code=400, detail="Invalid email address")

    # Check if user exists in the database
    db_user = get_user_by_username(username=username)
    if db_user:
        access_token, expire = create_access_token({"sub": username})
        user_info = generate_user_info(access_token, expire)
        redis_expiration = int((expire - datetime.now(timezone.utc)).total_seconds())
        redis_key = f"{db_user.id}"
        print("Updating Redis:", user_info)
        redis_client.setex(redis_key, redis_expiration, json.dumps(user_info))
    else:
        # If the user does not exist, create a new user
        user_data = UserCreate(username=username, name=username)
        db_user, access_token = create_user(user_data)

    return {"access_token": access_token, "token_type": "bearer"}


@login_router.post("/check-expiration")
async def check_expiration(background_tasks: BackgroundTasks):
    background_tasks.add_task(check_user_token_expiration)
    return {"message": "Checking for expired tokens in the background"}


@login_router.post("/logout")
def logout():
    # remove_redis_user()
    pass
