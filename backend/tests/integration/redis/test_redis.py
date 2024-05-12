import pytest
import time


from app.crud import get_user_by_username, redis_client


@pytest.mark.integration
class TestRedisOperations:
    def test_redis_stores_session_on_login(self, client, faker):
        from dotenv import load_dotenv
        load_dotenv()
        email = faker.email()
        login_data = {"username": email, "password": "secure_password"}
        client.post("/api/login/", data=login_data)
        time.sleep(1)
        user = get_user_by_username(email)
        session_data = redis_client.get(str(user.id)).decode("utf-8")
        redis_client.close()
        assert session_data is not None
