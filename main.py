#!/usr/bin/env python3


import logging.config
from app.logger.logging_settings import logging_config


logging.config.dictConfig(logging_config)


import asyncio
import logging


from app.bot import main
from config.config import Config, load_config

logger = logging.getLogger(__name__)
config: Config = load_config()


asyncio.run(main(config=config))
