import smtplib
from email.message import EmailMessage

from celery import Celery
from config import Config

app = Celery('tasks', broker=Config.REDIS_URL)


def get_email_template(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Отчет от telegram-budget' # за последний месяц/год/все время
    email['From'] = Config.SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        '<h2>Всего <за последний месяц/год/все время> Вы потратили Х рублей!</h2>'
        f'Здравствуте, {username}, здесь скро будет Ваш отчет'
        '<div>',
        subtype='html'
    )
    return email


@app.task
def send_email_report(username: str, user_email: str):
    """Отправляет заданному пользователю на почту отчет."""

    email = get_email_template(username, user_email)
    with smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT) as server:
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.send_message(email)
