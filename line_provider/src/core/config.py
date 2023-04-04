"""Settings"""
import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "..", "..")


class LineProvider(BaseSettings):
    project_name: str
    host: str
    port: int


class Settings(BaseSettings):
    line_provider: LineProvider

    class Config:
        env_file = (os.path.join(ENV_DIR, ".env"), os.path.join(ENV_DIR, ".env.dev"))
        env_nested_delimiter = "__"


settings = Settings()
