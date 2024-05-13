import pytest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import json

from app.crud import check_user_token_expiration


@pytest.fixture
def redis_data():
    return {
        "user:1": json.dumps(
            {
                "token_expires": (
                    datetime.now(timezone.utc) - timedelta(days=1)
                ).isoformat()
            }
        ),
        "user:2": json.dumps(
            {
                "token_expires": (
                    datetime.now(timezone.utc) + timedelta(days=1)
                ).isoformat()
            }
        ),
    }


@pytest.mark.unit
def test_check_user_token_expiration(redis_data):
    with patch("app.crud.redis_client.scan_iter", return_value=redis_data.keys()):
        with patch(
            "app.crud.redis_client.get",
            side_effect=lambda k: redis_data[k].encode("utf-8"),
        ):
            with patch("app.crud.redis_client.ttl", return_value=3600):
                with patch("app.crud.remove_user_from_database") as mock_remove:
                    check_user_token_expiration()
                    # Assert that remove_user_from_database is called with each user key
                    mock_remove.assert_any_call("user:1")
                    mock_remove.assert_any_call("user:2")
                    # Assert that remove_user_from_database is called exactly twice
                    assert mock_remove.call_count == 2

