# Суммаризатор сообщений VK
Бот сохраняет сообщения в базу данных и выдаёт по команде краткое изложение

## Стек
* Python 3.11, Docker
* Postgres, asyncpg
* aiohttp (запросы к DeepSeek)

## Начало работы

Создать файл `.env` на основе примера:
```shell
cp .env.example .env
```

Указать токен бота и токен Deepseek:
```dotenv
# .env
DB_USER=summarize
DB_PASSWORD=summarize
DB_NAME=summarize
DB_HOST=db
BOT_TOKEN=
DEEPSEEK_TOKEN=
```

Запустить проект через `docker compose`:
```
docker compose up -d --build
```

Посмотреть логи:
```shell
docker compose logs app -f 
```


Написать боту в личные сообщения или в чате команды
```
/help
```

Посмотреть краткое изложение обсуждений в чате:
```
/summary
```

