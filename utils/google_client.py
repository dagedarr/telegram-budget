# from aiogoogle import Aiogoogle
# from aiogoogle.auth.creds import ServiceAccountCreds

from google.oauth2 import service_account
from googleapiclient.discovery import build

from config import Config

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type': Config.TYPE,
    'project_id': Config.PROJECT_ID,
    'private_key_id': Config.PRIVATE_KEY_ID,
    'private_key': Config.PRIVATE_KEY,
    'client_email': Config.CLIENT_EMAIL,
    'client_id': Config.CLIENT_ID,
    'auth_uri': Config.AUTH_URI,
    'token_uri': Config.TOKEN_URI,
    'auth_provider_x509_cert_url': Config.AUTH_PROVIDER_X509_CERT_URL,
    'client_x509_cert_url': Config.CLIENT_X509_CERT_URL
}


def get_service(service: str, version: str):
    credentials = service_account.Credentials.from_service_account_info(
        INFO,
        scopes=SCOPES
    )

    service = build(service, version, credentials=credentials)
    yield service
