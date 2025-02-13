# project_2024.03.28

Сервис для загрузки и хранения файлов в защищенном хранилище дискового пространства сервера очень быстро разворачивается и сразу готов к работе.
Написан с применением технологий: 
- FastAPI
- Python 3.9.10
- Docker / Docker compose
- PostgreSQL 16.2 / asyncpg
- Uvicorn
- pydantic 2.10.6

Для развертывания необходимо склонировать репозиторий:
- Скопировать файл docker-compose.production.yml
- Создасть файл .env с необходимыми данными указанными в .env.example
- Запустить Docker
```sh
docker compose -f docker-compose.production.yml up
```

# Документация доступна по адресам:
- http://127.0.0.1:8000/docs

- http://127.0.0.1:8000/redoc
