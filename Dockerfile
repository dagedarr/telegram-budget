FROM python:3.11-slim

WORKDIR /telegram-budget

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
