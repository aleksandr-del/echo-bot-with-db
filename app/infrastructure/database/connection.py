#!/usr/bin/env python3


import logging
from psycopg import AsyncConnection, Error
from psycopg_pool import AsyncConnectionPool
from urllib.parse import quote
from config.config import Config


logger = logging.getLogger(__name__)


def build_pg_conninfo(config: Config) -> str:
    db = config.db
    conninfo = (
        f"postgresql://{quote(db.user, safe='')}:{quote(db.password, safe='')}"
        f"@{db.host}:{db.port}/{db.db_name}"
    )
    logger.info(
        (
            "Building PostgreSQL connection string "
            "(password omitted): postgresql://%s@%s:%s/%s"
        ),
        quote(db.user, safe=""),
        db.host,
        db.port,
        db.db_name,
    )
    return conninfo


async def log_db_version(connection: AsyncConnection) -> None:
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT version()")
            db_version = await cursor.fetchone()
            logger.info("Connected to PostgreSQL version: %s", db_version[0])
    except Error as err:
        logger.error("Failed to fetch DB version: %s", err)


async def get_pg_connection(config: Config) -> AsyncConnection:
    conninfo = build_pg_conninfo(config)
    connection: AsyncConnection | None = None

    try:
        connection = await AsyncConnection.connect(conninfo=conninfo, autocommit=True)
        await log_db_version(connection)
        return connection
    except Error as err:
        logger.error("Failed to connect to PostgreSQL: %s", err)
        if connection:
            await connection.close()
        raise


async def get_pg_pool(
    config: Config, min_size: int = 1, max_size: int = 3, timeout: float | None = 10.0
) -> AsyncConnectionPool:
    conninfo = build_pg_conninfo(config)
    db_pool: AsyncConnectionPool | None = None

    try:
        db_pool = AsyncConnectionPool(
            conninfo=conninfo,
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            open=False,
        )
        await db_pool.open()

        async with db_pool.connection() as connection:
            await log_db_version(connection)

        return db_pool
    except Error as err:
        logger.error("Failed to initialize PostgreSQL pool: %s", err)
        if db_pool and not db_pool.closed:
            await db_pool.close()
        raise
