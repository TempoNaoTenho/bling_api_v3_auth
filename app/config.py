import os
from pathlib import Path
from dotenv import load_dotenv

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Config():

    ##  Configs  ##

    BASE_DIR = Path(__file__).resolve().parent.parent
    ENV_FILE_PATHS = [
        BASE_DIR / '.env',
        Path(__file__).resolve().parent / '.env',
    ]
    for env_path in ENV_FILE_PATHS:
        load_dotenv(env_path)

    # Storage Method
    TOKENS_STORAGE_METHOD = os.environ.get('TOKENS_STORAGE_METHOD', 'json')

    ##  Secrets ##

    # BLING
    BLING_CLIENT_ID     = os.environ.get('BLING_CLIENT_ID')
    BLING_CLIENT_SECRET = os.environ.get('BLING_CLIENT_SECRET')

    # REDIS
    REDIS_HOST_IP       = os.environ.get('REDIS_HOST_IP')
    REDIS_HOST_PORT     = os.environ.get('REDIS_HOST_PORT')
    REDIS_PASSWORD      = os.environ.get('REDIS_PASSWORD')

    # Token handling defaults
    DEFAULT_ACCESS_TOKEN_EXPIRES_IN = int(os.environ.get('DEFAULT_ACCESS_TOKEN_EXPIRES_IN', '3600'))
    DEFAULT_REFRESH_TOKEN_EXPIRES_IN = int(os.environ.get('DEFAULT_REFRESH_TOKEN_EXPIRES_IN', '2592000'))
    ACCESS_TOKEN_EXPIRY_SKEW = int(os.environ.get('ACCESS_TOKEN_EXPIRY_SKEW', '60'))


class ConfigSingleton(_Config, metaclass=Singleton):
    pass
