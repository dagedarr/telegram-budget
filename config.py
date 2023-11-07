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
    PAGINATOR_BUTTONS: int = 5

    REDIS_URL: str = os.getenv('REDIS_URL')
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465

    SMTP_USER: str = os.getenv('SMTP_USER')  # Логин
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')  # Пароль
