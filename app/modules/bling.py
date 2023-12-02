import os
import json
import redis
import base64
import requests
import logging
from typing import Optional
from config import ConfigSingleton

LOGGER = logging.getLogger('django')

class TokenStorage:
    """
    A class to handle token storage and retrieval.
    """

    @staticmethod
    def check_param_value(param_name: str, param_value: str) -> None:
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
            raise ValueError(f'(check_param_value) - Missing params. Param: {param_name} Value: {param_value}')

        if isinstance(param_value, bytes):
            param_value = param_value.decode('utf-8')

        if not isinstance(param_value, str):
            raise TypeError('(check_param_value) - token_key_name must be a string')

    @staticmethod
    def save_token(token_key_name: str, token_value: str, expires_in: int = 21600) -> None:
        """
        Save a token with the given key name and value.

        Args:
            token_key_name (str): The name of the token key.
            token_value (str): The value of the token.
            expires_in (int, optional): The expiration time of the token in seconds. Defaults to 21600.
        """
        TokenStorage.check_param_value(param_name=token_key_name, param_value=token_value)

        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'redis':
            try:
                from modules import redis_client
                redis_client.RedisClient().set_bling_token(
                    access_token=token_key_name,
                    token_value=token_value,
                    expires_in=expires_in
                )
            except redis.RedisError as e:
                LOGGER.exception(e)
                raise
        elif ConfigSingleton.TOKENS_STORAGE_METHOD == 'json':
            credentials_folder = os.path.join(os.getcwd(), 'credential')
            os.makedirs(credentials_folder, exist_ok=True)
            credentials_file = os.path.join(credentials_folder, 'credentials.json')

            if not os.path.exists(credentials_file):
                with open(credentials_file, 'w') as file:
                    json.dump(
                        {
                            'access_token': '',
                            'refresh_token': '',
                            'expires_in': ''
                        },
                        file
                    )

            # Update the credentials file with the new token accordingly to the token_key_name
            with open(credentials_file, 'r') as file:
                credentials = json.load(file)

            credentials[token_key_name] = token_value

            with open(credentials_file, 'w') as file:
                json.dump(credentials, file)
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
        if ConfigSingleton.TOKENS_STORAGE_METHOD == 'redis':
            return redis.Redis(
                host=ConfigSingleton.REDIS_HOST_IP,
                port=ConfigSingleton.REDIS_HOST_PORT,
                password=ConfigSingleton.REDIS_PASSWORD,
                db=0
            ).get(token_key)
        elif ConfigSingleton.TOKENS_STORAGE_METHOD == 'json':
            credentials_folder = os.path.join(os.getcwd(), 'credential')
            credentials_file = os.path.join(credentials_folder, 'credentials.json')

            with open(credentials_file, 'r') as file:
                file_dict = json.load(file)

            return file_dict.get(token_key)
        else:
            raise NotImplementedError

class BlingApiTokenHandler:
    """
    A class for handling API token authentication for the Bling API.
    """
    AUTH_URL = 'https://www.bling.com.br/Api/v3/oauth/token'
    
    def __init__(self):
        self.headers = self._prepare_headers()

    def _prepare_headers(self):
        """
        Prepares the headers for the API request (must be in base64 {client_id}:{client_secret} format).
        """
        credential = f"{ConfigSingleton.BLING_CLIENT_ID}:{ConfigSingleton.BLING_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credential.encode('ascii')).decode('ascii')
        return {
            'Accept': '1.0',
            'Authorization': f'Basic {encoded_credentials}'
        }

    def _post_request(self, payload) -> dict:
        """
        Sends a POST request to the authentication endpoint.
        """
        response = requests.post(self.AUTH_URL, 
                                 headers=self.headers, json=payload)
        data = response.json()
        
        if response.status_code != 200:
            # Add more information to the error message or treat it
            data['status_code'] = response.status_code
            return data

        self._save_credentials(data)
        return data

    def _save_credentials(self, bling_response_dict):
        """
        Saves the access and refresh tokens to the token using TokenStorage class to handle custom storage options (e.g. Redis/Json).
        """
        access_token = bling_response_dict.get('access_token')
        refresh_token = bling_response_dict.get('refresh_token')
        expires_in = bling_response_dict.get('expires_in')
          
        if access_token:          
            TokenStorage.save_token(token_key_name='access_token', 
                                    token_value=access_token,
                                    expires_in=60)
            
        if refresh_token:
            TokenStorage.save_token(token_key_name='refresh_token', 
                                    token_value=refresh_token,
                                    expires_in=expires_in)

    def get_token_using_code(self, code) -> dict:
        """
        - Retrieves the access token using the URL code param. This code is used to get the access and refresh tokens. It has to be manually copied from the URL generated on Bling App Config.
        - Obtém o token de acesso usando o código URL. Este código é usado para obter os tokens de acesso e de atualização. Ele deve ser copiado manualmente da URL gerada no App Bling.
        """
        payload = {
            'Content-Type': 'application/x-www-form-urlencoded',
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
    
