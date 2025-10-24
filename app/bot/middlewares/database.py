#!/usr/bin/env python3


import logging
from typing import Any, Callable, Awaitable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Update
from psycopg_pool import AsyncConnectionPool


logger = logging.getLogger(__name__)
Data: TypeAlias = dict[str, Any]
Handler: TypeAlias = Callable[[Update, Data], Awaitable[Any]]


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Handler, event: Update, data: Data) -> Any:
        db_pool: AsyncConnectionPool | None = data.get("bd_pool")
        if db_pool is None:
            logger.error("Database pool is not provided in middleware data.")
            raise RuntimeError
        async with db_pool.connection() as connection:
            try:
                async with connection.transaction():
                    data["conn"] = connection
                    result = await handler(event, data)
            except Exception as err:
                logger.error("Transaction rolled back due to error: %s", err)
                raise
        return result
