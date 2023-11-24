import smtplib
from email.message import EmailMessage

from celery import Celery

from config import Config
from utils.google_client import get_service

app = Celery('tasks', broker=Config.REDIS_URL, backend=Config.REDIS_URL)


def get_email_template(user_email: str, subject: str, text: str):
    """Формирует письмо пользователю."""

    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = Config.SMTP_USER
    email['To'] = user_email

    email.set_content(
        text,
        subtype='html'
    )
    return email


@app.task
def send_email_statistic(user_email: str, subject: str, text: str):
    """Отправляет заданному пользователю на почту отчет."""

    email = get_email_template(user_email, subject, text)
    with smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT) as server:
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(email)


@app.task
def spreadsheets_create(label: str) -> str:
    for service in get_service(service='sheets', version='v4'):
        spreadsheet_body = {
            'properties': {
                'title': f'Отчет {label}',
                'locale': 'ru_RU'
            },
            'sheets': [{
                'properties':
                    {
                        'sheetType': 'GRID',
                        'sheetId': 0,
                        'title': 'Лист1'
                    }
            }]
        }
        response = service.spreadsheets().create(
            body=spreadsheet_body
        ).execute()
        spreadsheet_id = response['spreadsheetId']
        return spreadsheet_id


@app.task
def set_user_permissions(spreadsheet_id: str) -> None:
    for service in get_service(service='drive', version='v3'):
        permissions_body = {
            'type': 'anyone',
            'role': 'writer'
        }
        service.permissions().create(
            fileId=spreadsheet_id,
            body=permissions_body,
            fields='id'
        ).execute()


@app.task
def spreadsheets_update_value(spreadsheet_id: str, data: list) -> None:
    for service in get_service(service='sheets', version='v4'):
        update_body = {
            'majorDimension': 'ROWS',
            'values': data
        }
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:D{len(data)+10}',
            valueInputOption='USER_ENTERED',
            body=update_body
        ).execute()
