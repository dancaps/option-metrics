import os
import logging
from dotenv import load_dotenv

def get_log_level():
    level = os.getenv('LOG_LEVEL', 'INFO').upper()
    return getattr(logging, level, logging.INFO)

def get_env_var(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} not set in .env file")
    return value

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=get_log_level(), format="%(asctime)s [%(levelname)s] %(message)s")
DB_URL = get_env_var('DATABASE_URL')
FILE_PATH = get_env_var('FILE_PATH')
DATASOURCE = get_env_var('DATASOURCE')