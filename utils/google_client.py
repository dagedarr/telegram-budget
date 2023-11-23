from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

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

cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def get_service():
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        yield aiogoogle
