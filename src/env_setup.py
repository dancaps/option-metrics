import os
import logging
from dotenv import load_dotenv

def get_log_level():
    level = os.getenv('LOG_LEVEL', 'INFO').upper()
    return getattr(logging, level, logging.INFO)


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=get_log_level(), format="%(asctime)s [%(levelname)s] %(message)s")
DB_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:password@localhost:5432/postgres')
FILE_PATH = os.getenv('FILE_PATH', 'bucket/provider001/spx.txt')
DATASOURCE = os.getenv('DATASOURCE', 'PROVIDER001')