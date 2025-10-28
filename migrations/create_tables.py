#!/usr/bin/env python3


import logging
import logging.config
from app.logger.logging_settings import logging_config
import asyncio
from app.infrastructure.database.connection import get_pg_connection
from config.config import Config, load_config
from psycopg import AsyncConnection, Error


logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)
config: Config = load_config()


async def main():
    connection: AsyncConnection | None = None

    try:
        connection = await get_pg_connection(config=config)
        async with connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        query="""
                            create table if not exists users(
                                id serial primary key,
                                user_id bigint not null unique,
                                username varchar(50),
                                created_at timestamptz not null default now(),
                                language varchar(10) not null,
                                role varchar(30) not null,
                                is_alive boolean not null,
                                banned boolean not null
                                );
                            """
                    )
                    await cursor.execute(
                        query="""
                            create table if not exists activity(
                                id serial primary key,
                                user_id bigint references users(user_id),
                                created_at timestamptz not null default now(),
                                activity_date date not null default current_date,
                                actions int not null default 1
                                );
                            create unique index if not exists idx_activity_user_day on activity(user_id, activity_date);
                            """
                    )
                    logger.info(
                        "Tables `users` and `activity` have been successfully created"
                    )
    except Error as err:
        logger.error("Database error: %s", err)
    finally:
        if connection:
            await connection.close()
            logger.info("Connection to Postgres closed")


if __name__ == "__main__":
    asyncio.run(main())
