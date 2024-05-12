import pytest
from unittest.mock import patch
from datetime import datetime, timezone, timedelta
import json

from app.crud import check_user_token_expiration


@pytest.fixture
def redis_data():
    return {
        "user:1": json.dumps({"token_expires": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()}),
        "user:2": json.dumps({"token_expires": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()})
    }


@pytest.mark.unit
def test_check_user_token_expiration(redis_data):
    with patch("app.crud.redis_client.scan_iter", return_value=redis_data.keys()) as mock_scan:
        with patch("app.crud.redis_client.get", side_effect=lambda k: redis_data[k].encode('utf-8')) as mock_get:
            with patch("app.crud.redis_client.ttl", return_value=3600) as mock_ttl:
                with patch("app.crud.remove_user_from_database") as mock_remove:
                    check_user_token_expiration()
                    mock_remove.assert_called_once_with("user:1")
                    assert all('user:2' not in call.args[0] for call in mock_remove.call_args_list), "remove_user_from_database was called with user:2"
