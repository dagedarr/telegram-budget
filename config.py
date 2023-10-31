import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    API_TOKEN: str = os.getenv('API_TOKEN')
    DB_URL: str = os.getenv('DB_URL', '')  # mysql
    ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))

    LATEST_TRANSACTIONS_NUM: int = 5
