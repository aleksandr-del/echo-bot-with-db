#!/usr/bin/env python3


import logging
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update, TelegramObject, User
from app.infrastructure.database.db import get_user_banned_status_by_id
from psycopg import AsyncConnection
from .database import Data, Handler

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(self, handler: Handler, event: Update, data: Data) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        conn: AsyncConnection | None = data.get("conn")
        if conn is None:
            logger.error("Database connection not found in middleware data")
            raise RuntimeError
        user_banned_status = await get_user_banned_status_by_id(
            conn=conn, user_id=user.id
        )
        if user_banned_status:
            logger.info("Shadow-banned user tried to interact: %d", user.id)
            if event.callback_query:
                await event.callback_query.answer()
            return

        return await handler(event, data)
