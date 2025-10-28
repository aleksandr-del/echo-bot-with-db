# Echo Bot with Database

A Telegram bot built with aiogram 3.x that demonstrates PostgreSQL integration with multilingual support, user management, and admin features.

## Features

- **Echo functionality** - Responds to user messages
- **Multilingual support** - English and Russian languages
- **User management** - Registration, language preferences, activity tracking
- **Admin panel** - User banning, statistics, extended commands
- **Database integration** - PostgreSQL with connection pooling
- **Redis storage** - FSM state management
- **Shadow ban system** - Silent user restrictions
- **Activity counter** - User interaction tracking

## Tech Stack

- **Python 3.11+**
- **aiogram 3.22** - Telegram Bot API framework
- **PostgreSQL** - Primary database
- **Redis** - State storage and caching
- **psycopg** - PostgreSQL adapter
- **Docker & Docker Compose** - Containerization

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Telegram Bot Token (from @BotFather)

### Installation

1. Clone the repository:
```bash
git clone <https://github.com/aleksandr-del/echo-bot-with-db.git>
cd echo-bot-with-db
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your values
```

5. Start services:
```bash
docker-compose up -d
```

6. Run database migrations:
```bash
python migrations/create_tables.py
```

7. Start the bot:
```bash
python main.py
```

## Configuration

Edit `.env` file with your settings:

```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# PostgreSQL
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DATABASE=1
REDIS_USERNAME=default
REDIS_PASSWORD=your_redis_password
```

## Available Commands

### User Commands
- `/start` - Start/restart the bot
- `/help` - Show help message
- `/lang` - Change interface language

### Admin Commands
- `/ban` - Ban a user (reply to their message)
- `/unban` - Unban a user
- `/stats` - View bot statistics

## Project Structure

```
echo-bot-with-db/
├── app/
│   ├── bot/
│   │   ├── handlers/          # Message and callback handlers
│   │   ├── middlewares/       # Custom middlewares
│   │   ├── keyboards/         # Inline keyboards
│   │   ├── filters/           # Custom filters
│   │   ├── states/            # FSM states
│   │   ├── i18n/              # Internationalization
│   │   └── enums/             # Enumerations
│   ├── infrastructure/
│   │   └── database/         # Database operations
│   └── logger/               # Logging configuration
├── config/                   # Configuration management
├── locales/                  # Translation files
├── migrations/               # Database migrations
├── docker-compose.yml        # Docker services
├── requirements.txt          # Python dependencies
└── main.py                   # Application entry point
```

## Database Schema

The bot uses PostgreSQL with the following main tables:
- `users` - User information and preferences
- `activity` - Activity tracking
- Additional tables for bot functionality

## Development

### Adding New Languages

1. Create translation file in `locales/{lang}/txt.py`
2. Add language to `get_translations()` in `translator.py`
3. Update language keyboard in `keyboards.py`

### Adding New Handlers

1. Create handler in `app/bot/handlers/`
2. Register router in `bot.py`
3. Add necessary states in `states.py`

## Docker Deployment

The project includes Docker Compose configuration with:
- PostgreSQL database
- Redis cache
- PgAdmin (optional)

```bash
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
