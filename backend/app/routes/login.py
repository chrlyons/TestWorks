from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.crud import create_access_token

import re

login_router = APIRouter(prefix="/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@login_router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # Password cannot be 'password'
    if password == "password":
        raise HTTPException(status_code=400, detail="Password cannot be 'password'")

    # Regex for email validation
    email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    if not re.match(email_regex, username):
        raise HTTPException(status_code=400, detail="Invalid email address")

    # Create access token with the user's email as the subject
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
