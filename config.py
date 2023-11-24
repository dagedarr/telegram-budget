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

    DATE_FORMAT: str = '%d.%m.%Y'
    REDIS_URL: str = os.getenv('REDIS_URL')
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465

    SMTP_USER: str = os.getenv('SMTP_USER')  # Логин
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD')  # Пароль

    # ----------------------- GOOGLE API ------------------

    # FIRST_SUPERUSER_EMAIL: str = os.getenv('FIRST_SUPERUSER_EMAIL')
    # FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD')

    TYPE: str = os.getenv('TYPE')
    PROJECT_ID: str = os.getenv('PROJECT_ID')
    PRIVATE_KEY_ID: str = os.getenv('PRIVATE_KEY_ID')
    PRIVATE_KEY: str = os.getenv('PRIVATE_KEY')
    CLIENT_EMAIL: str = os.getenv('CLIENT_EMAIL')
    CLIENT_ID: str = os.getenv('CLIENT_ID')
    AUTH_URI: str = os.getenv('AUTH_URI')
    TOKEN_URI: str = os.getenv('TOKEN_URI')
    AUTH_PROVIDER_X509_CERT_URL: str = os.getenv('AUTH_PROVIDER_X509_CERT_URL')
    CLIENT_X509_CERT_URL: str = os.getenv('CLIENT_X509_CERT_URL')

    EMAIL: str = os.getenv('EMAIL')
