import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import json

from app.schema import UserCreate
from app.crud import (
    create_access_token,
    generate_user_info,
    create_user,
    get_token_expiration,
    is_token_expired,
    process_expired_token,
    check_user_token_expiration,
    remove_user_from_database,
    get_user_by_username,
    update_redis_user_session,
    remove_redis_user,
)

load_dotenv()


@pytest.mark.unit
class TestCrud:
    @patch("app.crud.redis_client")
    def test_create_access_token(self, mock_redis):
        import os

        secret = os.getenv("SECRET_KEY")
        algo = os.getenv("ALGORITHM")
        data = {"sub": "123"}
        expires_delta = timedelta(minutes=15)

        # Create the token
        token, expire = create_access_token(data, expires_delta)

        print(f"Generated token: {token}")
        print(f"Secret Key: {secret}")

        # Decode the token using the same secret key and algorithm
        decoded = jwt.decode(token, secret, algorithms=[algo])
        print(f"Decoded token: {decoded}")

        # Assert the claims
        assert decoded["sub"] == "123"
        assert isinstance(expire, datetime)

    def test_generate_user_info(self):
        access_token = "token"
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        user_info = generate_user_info(access_token, expire)

        assert user_info["status"] == "active"
        assert user_info["access_token"] == access_token
        assert user_info["token_expires"] == expire.isoformat()

    @patch("app.crud.get_db")
    @patch("app.crud.redis_client")
    def test_create_user(self, mock_redis, mock_get_db):
        user = UserCreate(username="testuser", name="Test User")
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        db_user, access_token = create_user(user)

        assert db_user.username == user.username
        assert isinstance(access_token, str)
        mock_redis.setex.assert_called()

    @patch("app.crud.redis_client")
    def test_get_token_expiration(self, mock_redis):
        mock_redis.ttl.return_value = 3600
        expiration = get_token_expiration("key")

        assert expiration == 3600

    def test_is_token_expired(self):
        expiration_time = (
            datetime.now(timezone.utc) + timedelta(minutes=-1)
        ).timestamp()
        expired = is_token_expired(expiration_time)

        assert expired is True

    @patch("app.crud.remove_redis_user")
    @patch("app.crud.remove_user_from_database")
    def test_process_expired_token(self, mock_remove_db, mock_remove_redis):
        user_id = "123"
        process_expired_token(user_id)

        mock_remove_redis.assert_called_with(user_id)
        mock_remove_db.assert_called_with(user_id)

    @pytest.mark.unit
    @patch("app.crud.redis_client")
    @patch("app.crud.get_db")
    def test_remove_invalid_user(self, mock_get_db, mock_redis_client):
        mock_db_session = MagicMock()
        mock_get_db.return_value = iter([mock_db_session])
        mock_db_session.query().filter().delete.side_effect = Exception(
            "Database error"
        )

        user_id = "invalid_user_id"
        remove_user_from_database(user_id)

        mock_db_session.rollback.assert_called_once()
        mock_redis_client.setex.assert_called_with(user_id, 600, "active")
        mock_redis_client.delete.assert_not_called()

    @patch("app.crud.redis_client")
    @patch("app.crud.get_token_expiration")
    @patch("app.crud.is_token_expired")
    @patch("app.crud.process_expired_token")
    def test_check_user_token_expiration(
        self, mock_process, mock_is_expired, mock_get_exp, mock_redis
    ):
        mock_redis.scan_iter.return_value = ["key1", "key2"]
        mock_get_exp.return_value = (
            datetime.now(timezone.utc) + timedelta(minutes=-1)
        ).timestamp()
        mock_is_expired.return_value = True

        check_user_token_expiration()

        mock_process.assert_called()

    @patch("app.crud.get_db")
    @patch("app.crud.redis_client")
    def test_remove_user_from_database(self, mock_redis, mock_get_db):
        user_id = "123"
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])

        remove_user_from_database(user_id)

        mock_db.query().filter().delete.assert_called()
        mock_db.commit.assert_called()
        mock_redis.delete.assert_called_with(user_id)

    @patch("app.crud.get_db")
    def test_get_user_by_username(self, mock_get_db):
        username = "testuser"
        mock_db = MagicMock()
        mock_user = MagicMock()
        mock_db.query().filter().first.return_value = mock_user
        mock_get_db.return_value = iter([mock_db])

        user = get_user_by_username(username)

        assert user == mock_user

    @patch("app.crud.redis_client")
    def test_update_redis_user_session(self, mock_redis):
        user_id = "123"
        session_info = {"session": "info"}

        update_redis_user_session(user_id, session_info)

        mock_redis.setex.assert_called_with(
            f"user_session:{user_id}", 3600, json.dumps(session_info)
        )

    @patch("app.crud.redis_client")
    def test_remove_redis_user(self, mock_redis):
        user_id = "123"

        remove_redis_user(user_id)

        mock_redis.delete.assert_called_with(user_id)
