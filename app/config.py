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
    
    BASE_DIR = Path(__file__).resolve().parent
    ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')
    load_dotenv(ENV_FILE_PATH)
    
    # Storage Method
    TOKENS_STORAGE_METHOD = 'json' # or 'redis' 

    ##  Secrets ##
        
    # BLING
    BLING_CLIENT_ID     = os.environ.get('BLING_CLIENT_ID')
    BLING_CLIENT_SECRET = os.environ.get('BLING_CLIENT_SECRET')  
    
    # REDIS
    REDIS_HOST_IP       = os.environ.get('REDIS_HOST_IP')
    REDIS_HOST_PORT     = os.environ.get('REDIS_HOST_PORT')
    REDIS_PASSWORD      = os.environ.get('REDIS_PASSWORD')


class ConfigSingleton(_Config, metaclass=Singleton):
    pass