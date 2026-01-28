try:
    import redis  # type: ignore
except ModuleNotFoundError as exc:  # pragma: no cover - guarded import
    raise ModuleNotFoundError(
        'Redis dependency not installed. Install with '
        '`pip install -r requirements-redis.txt` or set '
        'TOKENS_STORAGE_METHOD=json.'
    ) from exc

from config import ConfigSingleton

class RedisConn:
    """A class to handle Redis connection."""

    HOST = ConfigSingleton.REDIS_HOST_IP or '127.0.0.1'
    PORT = int(ConfigSingleton.REDIS_HOST_PORT or 6379)
    PASSWORD = ConfigSingleton.REDIS_PASSWORD

    redis_connection = redis.Redis(host=HOST, port=PORT, password=PASSWORD, db=0)

class RedisClient(RedisConn):
    """A class to handle Redis operations."""

    def set_bling_token(self, token_name: str,
                        token_value: str=None,
                        expires_in: int=21600):
        """
        Set the Bling token in Redis.

        Args:
        - token_name: The name of the token.
        - token_value: The value of the token.
        - expires_in: The time in seconds until the token expires.
        """
        if token_name in ['access_token', 'refresh_token']:
            self.redis_connection.setex(token_name, expires_in, token_value)

    def get_current_bling_access_token(self):
        """
        Get the current Bling access token from Redis.

        Returns:
        - The current Bling access token as a string, or None if the token is not found.
        """
        access_token = self.redis_connection.get('access_token')

        if access_token:
            return access_token.decode('utf-8')
        return None

    def get_current_bling_refresh_token(self):
        """
        Get the current Bling refresh token from Redis.

        Returns:
        - The current Bling refresh token as a string, or None if the token is not found.
        """
        refresh_token = self.redis_connection.get('refresh_token')

        if refresh_token:
            return refresh_token.decode('utf-8')
        return None
