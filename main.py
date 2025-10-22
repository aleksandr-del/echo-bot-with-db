#!/usr/bin/env python3

import asyncio
from config.config import Config, load_config
from migrations.create_tables import main


if __name__ == "__main__":
    asyncio.run(main())
