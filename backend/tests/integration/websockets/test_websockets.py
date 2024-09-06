import pytest
from starlette.testclient import TestClient, WebSocketDisconnect
from unittest.mock import patch

import jwt
from app.main import app


class MockUser:
    id = 1
    username = "test@example.com"


@pytest.mark.integration
def test_websocket_endpoint_accepts_valid_token():
    client = TestClient(app)
    valid_token = jwt.encode({"sub": "test@example.com"}, "secret", algorithm="HS256")

    with patch("jwt.decode", return_value={"sub": "test@example.com"}):
        with patch("app.crud.get_user_by_username", return_value=MockUser()):
            with patch("redis.Redis.ttl", return_value=3600):
                with client.websocket_connect(
                    f"/api/ws/test@example.com?access_token={valid_token}"
                ) as websocket:
                    data = websocket.receive_json()
                    expected_time = 3600
                    actual_time = int(data["message"].split(": ")[1].split(" ")[0])
                    assert (
                        abs(actual_time - expected_time) <= 10
                    ), "Session time is not within the expected range"


@pytest.mark.integration
def test_websocket_endpoint_rejects_invalid_token():
    client = TestClient(app)
    invalid_token = "not.a.valid.token"

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            f"/api/ws/test@example.com?token={invalid_token}"
        ) as websocket:
            websocket.receive_json()

    assert (
        exc_info.value.code == 1008
    ), "Expected closure code for invalid token not received"


@pytest.mark.integration
def test_websocket_endpoint_closes_on_missing_token():
    client = TestClient(app)

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect("/api/ws/test@example.com") as websocket:
            websocket.receive_json()

    assert (
        exc_info.value.code == 1008
    ), "Expected closure code for missing token not received"


@pytest.mark.integration
def test_websocket_endpoint_closes_on_jwt_error():
    client = TestClient(app)
    invalid_token = "not.a.valid.token"

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect(
            f"/api/ws/test@example.com?token={invalid_token}"
        ) as websocket:
            websocket.receive_json()

    assert (
        exc_info.value.code == 1008
    ), "Expected closure code for JWT error not received"


@pytest.mark.integration
def test_websocket_endpoint_closes_on_jwt_error_missing_algorithm():
    client = TestClient(app)
    valid_token = jwt.encode({"sub": "test@example.com"}, "secret", algorithm="HS256")

    with pytest.raises(WebSocketDisconnect) as exc_info:
        with patch("jwt.decode", side_effect=jwt.JWTError("Missing algorithm")):
            with client.websocket_connect(
                f"/api/ws/test@example.com?token={valid_token}"
            ) as websocket:
                websocket.receive_json()

    assert (
        exc_info.value.code == 1008
    ), "Expected closure code for JWT error (missing algorithm) not received"


@pytest.mark.integration
def test_websocket_endpoint_closes_on_redis_key_absence():
    client = TestClient(app)
    valid_token = jwt.encode({"sub": "test@example.com"}, "secret", algorithm="HS256")

    with patch("app.crud.get_user_by_username", return_value=MockUser()):
        with patch("redis.Redis.exists", return_value=False):
            with pytest.raises(WebSocketDisconnect) as exc_info:
                with client.websocket_connect(
                    f"/api/ws/test@example.com?token={valid_token}"
                ) as websocket:
                    websocket.receive_json()

    assert (
        exc_info.value.code == 1008
    ), "Expected closure code for Redis key absence not received"


@pytest.mark.integration
def test_websocket_endpoint_handles_websocket_disconnect_exception():
    client = TestClient(app)
    valid_token = jwt.encode({"sub": "test@example.com"}, "secret", algorithm="HS256")

    with patch("app.crud.get_user_by_username", return_value=MockUser()):
        with patch("redis.Redis.exists", side_effect=WebSocketDisconnect):
            with client.websocket_connect(
                f"/api/ws/test@example.com?token={valid_token}"
            ):
                pass
