import base64
import json
import os
import time
from typing import Optional, Tuple

import requests

from config import ConfigSingleton

class BlingApiError(RuntimeError):
    """Raised when the Bling auth API returns an error."""

class TokenStorage:
    """A class to handle token storage and retrieval."""

    CREDENTIALS_DIRNAME = 'credential'
    CREDENTIALS_FILENAME = 'credentials.json'

    @staticmethod
    def check_param_value(param_name: str, param_value: str):
        """
        Check if the parameter name and value are valid.

        Args:
            param_name (str): The name of the parameter.
            param_value (str): The value of the parameter.

        Raises:
            ValueError: If the parameter name or value is missing.
            TypeError: If the parameter value is not a string.
        """
        if not param_value or not param_name:
            raise ValueError(
                f'(check_param_value) - Missing params. Param: {param_name} Value: {param_value}')

        if isinstance(param_value, bytes):
            param_value = param_value.decode('utf-8')

        if not isinstance(param_value, str):
            raise TypeError('(check_param_value) - token_key_name must be a string')

    @staticmethod
    def _credentials_path() -> str:
        credentials_folder = os.path.join(ConfigSingleton.BASE_DIR, TokenStorage.CREDENTIALS_DIRNAME)
        return os.path.join(credentials_folder, TokenStorage.CREDENTIALS_FILENAME)

    @staticmethod
    def _ensure_credentials_file() -> None:
        credentials_file = TokenStorage._credentials_path()
        credentials_folder = os.path.dirname(credentials_file)
        os.makedirs(credentials_folder, exist_ok=True)

        if not os.path.exists(credentials_file):
            with open(credentials_file, 'w', encoding='utf-8') as file:
                json.dump(
                    {
                        'access_token': '',
                        'access_token_expires_in': '',
                        'access_token_obtained_at': '',
                        'refresh_token': '',
                        'refresh_token_expires_in': '',
                        'refresh_token_obtained_at': ''
                    },
                    file
                )
            os.chmod(credentials_file, 0o600)

    @staticmethod
    def _metadata_keys(token_key_name: str) -> Tuple[str, str]:
        return (f'{token_key_name}_expires_in', f'{token_key_name}_obtained_at')

    @staticmethod
    def save_token(token_key_name: str,
                   token_value: str,
                   expires_in: Optional[int] = None,
                   obtained_at: Optional[int] = None):
        """
        Save a token with the given key name and value.

        Args:
            token_key_name (str): The name of the token key.
            token_value (str): The value of the token.
            expires_in (int, optional): The expiration time of the token in seconds.
            obtained_at (int, optional): Unix timestamp when the token was obtained.
        """
        TokenStorage.check_param_value(param_name=token_key_name, param_value=token_value)

        if expires_in is None:
            if token_key_name == 'access_token':
                expires_in = ConfigSingleton.DEFAULT_ACCESS_TOKEN_EXPIRES_IN
            elif token_key_name == 'refresh_token':
                expires_in = ConfigSingleton.DEFAULT_REFRESH_TOKEN_EXPIRES_IN

        if obtained_at is None:
            obtained_at = int(time.time())

        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'redis':
            try:
                import redis  # type: ignore
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    'Redis dependency not installed. Install with '
                    '`pip install -r requirements-redis.txt` or set '
                    'TOKENS_STORAGE_METHOD=json.'
                ) from exc
            try:
                from modules import redis_client
                redis_client_instance = redis_client.RedisClient()

                redis_client_instance.set_bling_token(
                    token_name=token_key_name,
                    token_value=token_value,
                    expires_in=expires_in
                )
            except redis.RedisError as e:
                print(e)
                raise
        elif ConfigSingleton.TOKENS_STORAGE_METHOD == 'json':
            TokenStorage._ensure_credentials_file()
            credentials_file = TokenStorage._credentials_path()

            with open(credentials_file, 'r', encoding='utf-8') as file:
                credentials = json.load(file)

            credentials[token_key_name] = token_value
            expires_in_key, obtained_at_key = TokenStorage._metadata_keys(token_key_name)
            if expires_in is not None:
                credentials[expires_in_key] = expires_in
            if obtained_at is not None:
                credentials[obtained_at_key] = obtained_at

            with open(credentials_file,
                      'w',
                      encoding='utf-8') as file:
                json.dump(credentials, file)
            os.chmod(credentials_file, 0o600)
        else:
            raise NotImplementedError

    @staticmethod
    def retrieve_token_by_key(token_key: str) -> Optional[str]:
        """
        Retrieve a token value given a token key.

        Args:
            token_key (str): The key of the token.

        Returns:
            Optional[str]: The value of the token if found, None otherwise.
        """

        token = None
        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'redis':
            try:
                import redis  # type: ignore
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    'Redis dependency not installed. Install with '
                    '`pip install -r requirements-redis.txt` or set '
                    'TOKENS_STORAGE_METHOD=json.'
                ) from exc

            token = redis.Redis(
                host=ConfigSingleton.REDIS_HOST_IP,
                port=ConfigSingleton.REDIS_HOST_PORT,
                password=ConfigSingleton.REDIS_PASSWORD,
                db=0
            ).get(token_key)

            if isinstance(token, bytes):
                token = token.decode('utf-8')

        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'json':
            credentials_file = TokenStorage._credentials_path()
            if not os.path.exists(credentials_file):
                return None

            with open(credentials_file, 'r', encoding='utf-8') as file:
                file_dict = json.load(file)

            token = file_dict.get(token_key)

        return token

    @staticmethod
    def is_token_expired(token_key: str) -> bool:
        """
        Check if a token is expired based on stored metadata or Redis TTL.
        """
        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'redis':
            try:
                import redis  # type: ignore
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    'Redis dependency not installed. Install with '
                    '`pip install -r requirements-redis.txt` or set '
                    'TOKENS_STORAGE_METHOD=json.'
                ) from exc

            redis_client = redis.Redis(
                host=ConfigSingleton.REDIS_HOST_IP,
                port=ConfigSingleton.REDIS_HOST_PORT,
                password=ConfigSingleton.REDIS_PASSWORD,
                db=0
            )
            ttl = redis_client.ttl(token_key)
            if ttl is None or ttl == -2:
                return True
            if ttl == -1:
                return False
            return ttl <= ConfigSingleton.ACCESS_TOKEN_EXPIRY_SKEW

        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'json':
            credentials_file = TokenStorage._credentials_path()
            if not os.path.exists(credentials_file):
                return True

            with open(credentials_file, 'r', encoding='utf-8') as file:
                file_dict = json.load(file)

            expires_in_key, obtained_at_key = TokenStorage._metadata_keys(token_key)
            expires_in = file_dict.get(expires_in_key)
            obtained_at = file_dict.get(obtained_at_key)

            if not expires_in or not obtained_at:
                return True

            try:
                expires_in = int(expires_in)
                obtained_at = int(obtained_at)
            except (TypeError, ValueError):
                return True

            now = int(time.time())
            return now >= (obtained_at + expires_in - ConfigSingleton.ACCESS_TOKEN_EXPIRY_SKEW)

        return True

class BlingApiTokenHandler:
    """
    A class for handling API token authentication for the Bling API.
    """
    AUTH_URL = 'https://www.bling.com.br/Api/v3/oauth/token'

    def __init__(self):
        self.headers = self._prepare_headers()

    def _prepare_headers(self):
        """
        Prepares the headers for the API request
        (must be in base64 {client_id}:{client_secret} format).
        """
        if not ConfigSingleton.BLING_CLIENT_ID or not ConfigSingleton.BLING_CLIENT_SECRET:
            raise ValueError('Missing BLING_CLIENT_ID or BLING_CLIENT_SECRET')

        credential = f"{ConfigSingleton.BLING_CLIENT_ID}:{ConfigSingleton.BLING_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credential.encode('ascii')).decode('ascii')
        return {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_credentials}'
        }

    def _post_request(self, payload):
        """
        Sends a POST request to the authentication endpoint.
        """
        headers = {
            **self.headers,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(self.AUTH_URL,
                                     headers=headers,
                                     data=payload,
                                     timeout=10)
        except requests.RequestException as exc:
            raise BlingApiError(f'Bling auth request failed: {exc}') from exc

        data = {}
        content_type = response.headers.get('Content-Type', '').lower()
        if 'application/json' in content_type:
            try:
                data = response.json()
            except ValueError:
                data = {'error': 'invalid_json', 'raw': response.text}
        else:
            data = {'raw': response.text}

        if not response.ok:
            message = data.get('error_description') or data.get('error') or response.text
            raise BlingApiError(f'Bling auth error ({response.status_code}): {message}')

        self._save_credentials(data)
        return data

    def _save_credentials(self, bling_response_dict):
        """
        Saves the access and refresh tokens to the token using TokenStorage
        class to handle custom storage options (e.g. Redis/Json).
        """
        access_token = bling_response_dict.get('access_token')
        refresh_token = bling_response_dict.get('refresh_token')
        access_expires_in = bling_response_dict.get('expires_in')
        refresh_expires_in = bling_response_dict.get('refresh_token_expires_in')

        try:
            access_expires_in = int(access_expires_in) if access_expires_in else None
        except (TypeError, ValueError):
            access_expires_in = None

        try:
            refresh_expires_in = int(refresh_expires_in) if refresh_expires_in else None
        except (TypeError, ValueError):
            refresh_expires_in = None

        if access_token:
            TokenStorage.save_token(token_key_name='access_token',
                                    token_value=access_token,
                                    expires_in=access_expires_in)

        if refresh_token:
            TokenStorage.save_token(token_key_name='refresh_token',
                                    token_value=refresh_token,
                                    expires_in=refresh_expires_in)

    def get_token_using_code(self, code):
        """
        - Retrieves the access token using the URL code param.
          This code is used to get the access and refresh tokens.
          It has to be manually copied from the URL generated on Bling App Config.

        - Obtém o token de acesso usando o código URL.
          Este código é usado para obter os tokens de acesso e de atualização.
          Ele deve ser copiado manualmente da URL gerada no App Bling.
        """
        payload = {
            'grant_type': 'authorization_code',
            'code': code
        }

        return self._post_request(payload)

    def refresh_tokens(self, refresh_token) -> dict:
        """
        - Refreshes the access and refresh tokens using the refresh token.
        - Atualiza os tokens de acesso e de atualização usando o token de atualização.
        """
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        return self._post_request(payload)
