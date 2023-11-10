FROM python:3.11-slim

RUN mkdir /telegram-budget

WORKDIR /telegram-budget

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod a+x infra/tg_bot.sh