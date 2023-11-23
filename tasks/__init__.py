from celery import Celery

from config import Config

app = Celery('tasks', broker=Config.REDIS_URL)
