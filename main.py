#!/usr/bin/env python3

import logging.config
from app.logger.logging_settings import logging_config

logging.config.dictConfig(logging_config)

import asyncio
from app.infrastructure.database.connection import get_pg_connection
from app.infrastructure.database.db import (
    add_user,
    get_user,
    update_user_alive_status,
    update_user_activity,
    update_user_lang,
    get_user_role,
)
from config.config import Config, load_config


async def main():
    config: Config = load_config()
    conn = await get_pg_connection(config=config)
    await add_user(conn, user_id=852456, username="Alex")
    await update_user_activity(conn, user_id=852456)
    await update_user_activity(conn, user_id=852456)
    await update_user_alive_status(conn, is_alive=False, user_id=852456)
    await update_user_lang(conn, language="en", user_id=852456)
    role = await get_user_role(conn, user_id=852456)
    user = await get_user(conn, 852456)
    return user, role


if __name__ == "__main__":
    print(asyncio.run(main()))
