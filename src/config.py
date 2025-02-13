import os
from typing import ClassVar

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRESS_DB_USER: str = os.getenv('POSTGRESS_DB_USER')
    POSTGRESS_DB_PASSWORD: str = os.getenv('POSTGRESS_DB_PASSWORD')
    DB_DATABASE: str = os.getenv('DB_DATABASE')
    DB_PORT: str = os.getenv('DB_PORT')
    DATABASE_URL: ClassVar[str] = (
        f'postgresql+asyncpg://{POSTGRESS_DB_USER}:'
        f'{POSTGRESS_DB_PASSWORD}@db:{DB_PORT}/{DB_DATABASE}'
    )

    class Config:
        env_file = '.env'


settings = Settings()
