# https://t.me/natolinbot
## Свяжитесь со мной если сервис недоступен

# Финансовый ассистент на базе телеграм бота

Этот проект представляет собой телеграм-бота, созданного с использованием Python и aiogram, который помогает вести учет личных финансов. Бот позволяет пользователям управлять категориями трат, устанавливать алиасы для них, а также получать статистику расходов в удобном формате.

Также в боте реализована версия для деплоя на pythonanywhere с использованием flask (вебхук)

Aiogram Flask template with webhooks to deploy to pythonanywhere free plan

# Основные функции
- Добавление категорий трат: Пользователи могут создавать категории для учета различных расходов.
- Установка алиасов: Для удобства ввода пользователи могут устанавливать алиасы для категорий трат.
- Статистика расходов: Бот предоставляет подробную статистику расходов по категориям.
- Уведомления по почте: Используя Celery и Redis, бот может отправлять уведомления о финансовых операциях по электронной почте либо дать ссылку на гугл таблицу.
- Реализован вебхук для корректной работы на бесплатном тарифе pythonanywhere

Более подробно с функциями бота можно ознакомиться через /help в самом [боте!](https://t.me/natolinbot)

# Установка

1. Клонируйте репозиторий
```
git clone https://github.com/dagedarr/StoreProject.git

cd telegram-budget/
```
Если вы не используете Git, то вы можете просто скачать исходный код репозитория в ZIP-архиве и распаковать его на свой компьютер.

2. Переименуйте .env.example в .env и следуйте инструкциям внутри этого файла

## Если вы используете Docker:

3. Запустите docker-compose

```
cd infra/

docker-compose up -d
```
4. В случае некорректной работы контейнера telegram-budget перезапустите контейнеры:

```
docker-compose stop
docker-compose up -d
```

## Если Вы не используете Docker

3. В директории telegram-budget выполните следующие команды:

```
python main.py

celery -A tasks.tasks:app worker --loglevel=INFO --pool=solo

celery -A tasks.tasks:app flower
```

# Готово!
Вы успешно установили бота и готовы начать его использовать!

# Вклад в проект
Если у вас есть предложения по улучшению или вы обнаружили баг, не стесняйтесь создать issue, отправить pull request либо написать напрямую автору. Ваш вклад приветствуется!

# Автор
[Натолин Артем](https://github.com/dagedarr)

[Ссылка на еще один мой проект - интернет магазин на Django](https://github.com/dagedarr/StoreProject) 
