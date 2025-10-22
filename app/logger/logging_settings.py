from .logging_filters import ErrorLogFilter, InfoLogFilter

logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "error_formatter": {
            "format": (
                "%(levelname)s - [%(asctime)s] - %(filename)s:"
                "%(lineno)d - %(name)s:%(funcName)s - %(message)s"
            ),
            "style": "%",
        },
        "info_formatter": {
            "format": "%(levelname)s - [%(asctime)s] - %(name)s - %(message)s",
            "style": "%",
        },
    },
    "filters": {
        "error_filter": {"()": ErrorLogFilter},
        "info_filter": {"()": InfoLogFilter},
    },
    "handlers": {
        "error_handler": {
            "class": "logging.FileHandler",
            "formatter": "error_formatter",
            "filters": ["error_filter"],
            "filename": "./error.log",
            "mode": "w",
        },
        "info_handler": {
            "class": "logging.FileHandler",
            "formatter": "info_formatter",
            "filters": ["info_filter"],
            "filename": "./info.log",
            "mode": "w",
        },
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["error_handler", "info_handler"]}
    },
}
