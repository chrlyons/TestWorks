from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
from os import getenv
import redis
from app.models import User
from app.schema import UserCreate
from app.database import get_db

from urllib.parse import urlparse
import json

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
REDIS_URL = getenv("REDIS_URL")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


redis_url = urlparse(REDIS_URL)
redis_client = redis.Redis(
    host=redis_url.hostname,
    port=redis_url.port,
    db=int(redis_url.path[1:] if redis_url.path else 0),
)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def generate_user_info(access_token, expire):
    return {
        "status": "active",
        "last_login": datetime.now(timezone.utc).isoformat(),
        "access_token": access_token,
        "token_expires": expire.isoformat(),
    }


def create_user(user: UserCreate):
    from json import dumps

    db = next(get_db())

    db_user = User(username=user.username, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token, expire = create_access_token({"sub": str(db_user.id)})

    user_info = generate_user_info(access_token, expire)

    # Calculate the expiration time for Redis entry
    redis_expiration = int((expire - datetime.now(timezone.utc)).total_seconds())

    # Set or reset the expiration time every time this function is called
    redis_key = f"{db_user.id}"
    redis_client.setex(redis_key, redis_expiration, dumps(user_info))

    return db_user, access_token


def get_current_time():
    return datetime.now(timezone.utc)


def get_token_expiration(key):
    expiration = redis_client.ttl(key)
    return expiration


def get_value_data(key):
    value = redis_client.get(key)
    try:
        value_data = json.loads(value)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON for key {key}: {e}")
        return None
    return value_data


def is_token_expired(expiration_time, current_time):
    return current_time > expiration_time


def process_expired_token(user_id):
    remove_user_from_database(user_id)


def check_user_token_expiration():
    current_time = get_current_time()
    for key in redis_client.scan_iter("*"):
        expiration = get_token_expiration(key)

        if expiration:
            value_data = get_value_data(key)
            if value_data and "token_expires" in value_data:
                expiration_time = datetime.fromisoformat(value_data["token_expires"])
                if expiration_time.tzinfo is None:
                    expiration_time = expiration_time.replace(tzinfo=timezone.utc)

                if is_token_expired(expiration_time, current_time):
                    user_id = key
                    process_expired_token(user_id)


def remove_user_from_database(user_id: str):
    db = next(get_db())
    try:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
        redis_client.delete(user_id)
    except Exception as e:
        db.rollback()
        print(f"Failed to delete user {user_id} from database: {e}")
        redis_client.setex(user_id, 600, "active")


def get_user_by_username(username: str):
    db = next(get_db())
    return db.query(User).filter(User.username == username).first()


def update_redis_user_session(user_id, session_info):
    # This function should update the Redis store with new session information
    redis_client.setex(f"user_session:{user_id}", 3600, json.dumps(session_info))
