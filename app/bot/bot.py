#!/usr/bin/env python3

import logging.config
from app.logger.logging_settings import logging_config

logging.config.dictConfig(logging_config)

import psycopg_pool
import logging
from redis.asyncio import Redis

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.bot.handlers import admin_router, others_router, settings_router, user_router
from app.bot.i18n.translator import get_translations
from app.infrastructure.database.connection import get_pg_pool
from app.bot.middlewares import (
    DataBaseMiddleware,
    TranslatorMiddlware,
    LangSettingsMiddlware,
    ShadowBanMiddleware,
    ActivityCounterMiddleware,
)

from config.config import Config


logger = logging.getLogger(__name__)


async def main(config: Config) -> None:
    logger.info("Starting bot ....")

    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            username=config.redis.username,
            password=config.redis.password,
        )
    )
    bot = Bot(
        token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(config=config)
    translations = get_translations()
    locales = list(translations.keys())

    logger.info("Registering routers ...")
    dp.include_routers(settings_router, admin_router, user_router, others_router)

    logger.info("Registering custom middlewares ...")
    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(ShadowBanMiddleware())
    dp.update.middleware(ActivityCounterMiddleware())
    dp.update.middleware(LangSettingsMiddlware())
    dp.update.middleware(TranslatorMiddlware())

    try:
        await dp.start_polling(
            bot,
            db_pool=db_pool,
            translations=translations,
            locales=locales,
            admin_ids=config.bot.admin_ids,
        )
    except Exception as err:
        logger.error(err)
    finally:
        await db_pool.close()
        logger.info("Connection to Postgres closed")
