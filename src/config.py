import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRESS_DB_USER: str = os.getenv('POSTGRESS_DB_USER')
    POSTGRESS_DB_PASSWORD: str = os.getenv('POSTGRESS_DB_PASSWORD')
    DATABASE_URL = (
        f'postgresql+asyncpg://{POSTGRESS_DB_USER}:'
        f'{POSTGRESS_DB_PASSWORD}@db:5432/fastapi_db'
    )

    class Config:
        env_file = '.env'


settings = Settings()
