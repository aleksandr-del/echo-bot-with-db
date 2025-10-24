#!/usr/bin/env python3


import logging
from re import A
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update, User
from aiogram.fsm.context import FSMContext
from psycopg import AsyncConnection
from app.infrastructure.database.db import get_user_lang
from .database import Handler, Data


logger = logging.getLogger(__name__)


class TranslatorMiddlware(BaseMiddleware):
    async def __call__(self, handler: Handler, event: Update, data: Data) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        state: FSMContext = data.get("state")
        user_context_data = state.get_data()

        if (user_lang := user_context_data.get("user_lang")) is None:
            conn: AsyncConnection | None = data.get("conn")
            if conn is None:
                logger.error("Database connection not found in middleware data")
                raise RuntimeError
            user_lang: str | None = await get_user_lang(conn=conn, user_id=user.id)
            user_lang = user_lang or user.language_code

        translations: dict = data.get("translations")
        i18n: dict = translations.get(user_lang)

        data["i18n"] = i18n or translations[translations["default"]]

        return await handler(event, data)
