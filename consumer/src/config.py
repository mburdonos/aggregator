"""Settings"""
import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_DIR = os.path.join(BASE_DIR, "..", "..")

class BetMaker(BaseSettings):
    project_name: str
    host: str
    port: int
    protocol: str = "http"
    path_event_url: str = "/api/v1/bet/update"

class RabbitMq(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    queue_events: str


class Settings(BaseSettings):
    bet_maker: BetMaker
    rabbitmq: RabbitMq

    class Config:
        env_file = (os.path.join(ENV_DIR, ".env"), os.path.join(ENV_DIR, ".env.dev"))
        env_nested_delimiter = "__"


settings = Settings()
