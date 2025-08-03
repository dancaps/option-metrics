import os
import logging
from dotenv import load_dotenv


def get_log_level(level):
    return getattr(logging, level, logging.INFO)

# Loading environment variables from .env file
load_dotenv()

# These can be overridden by .env file or environment variables
DB_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:password@localhost:5432/postgres')
FILE_PATH = os.getenv('FILE_PATH', 'bucket/provider001/spx.txt')
DATASOURCE = os.getenv('DATASOURCE', 'PROVIDER001')
LOGGING_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=get_log_level(LOGGING_LEVEL), format="%(asctime)s [%(levelname)s] %(message)s")