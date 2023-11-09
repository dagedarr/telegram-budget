import smtplib
from email.message import EmailMessage

from celery import Celery

from config import Config

app = Celery('tasks', broker=Config.REDIS_URL)


def get_email_template(user_email: str, subject: str, text: str):
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
