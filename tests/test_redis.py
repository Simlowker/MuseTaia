from unittest.mock import patch, MagicMock
from app.core.redis_client import get_redis_client

def test_redis_set_get():
    with patch("redis.Redis") as mock_redis_class:
        mock_client = MagicMock()
        mock_redis_class.return_value = mock_client
        
        client = get_redis_client()
        client.set("key", "value")
        mock_client.set.assert_called_once_with("key", "value")
        
        mock_client.get.return_value = b"value"
        val = client.get("key")
        assert val == b"value"
        mock_client.get.assert_called_once_with("key")
