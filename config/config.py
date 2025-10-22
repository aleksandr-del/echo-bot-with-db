import logging
import logging.config
import os
from environs import Env
from environs.exceptions import EnvError
from dataclasses import dataclass
from app.logger.logging_settings import logging_config

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str
    admin_ids: list[int]


@dataclass
class DatabaseSettings:
    db_name: str
    host: str
    port: int
    user: str
    password: str


@dataclass
class RedisSettings:
    host: str
    port: int
    db: int
    password: str
    username: str


@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings


def load_config(path: str | None = None) -> Config:
    env = Env()

    try:
        env.read_env(path)
    except ValueError as err:
        logger.error(err)
        raise
    try:
        token: str = env("BOT_TOKEN")
        if not token:
            logger.error("BOT_TOKEN must not be empty")
            raise ValueError
        raw_ids: list[int] = env.list("ADMIN_IDS", default=[])
        try:
            admin_ids: list[int] = [int(id) for id in raw_ids]
        except ValueError:
            logger.error("ADMIN_IDS must be integers, got: %s", raw_ids)
            raise
        bot = BotSettings(token=token, admin_ids=admin_ids)
        db = DatabaseSettings(
            db_name=env("POSTGRES_DB"),
            host=env("POSTGRES_HOST"),
            port=env("POSTGRES_PORT"),
            user=env("POSTGRES_USER"),
            password=env("POSTGRES_PASSWORD"),
        )
        redis = RedisSettings(
            host=env("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            db=env.int("REDIS_DATABASE"),
            password=env("REDIS_PASSWORD", default=""),
            username=env("REDIS_USERNAME", default=""),
        )
    except EnvError as err:
        logger.error(err)
        raise

    logger.info("Configuration loaded successfully")

    return Config(bot=bot, db=db, redis=redis)
