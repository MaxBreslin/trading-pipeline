import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

log_dir = "logs/"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(
    log_dir, f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)


def setup_logging() -> None:
    if logging.getLogger().hasHandlers():
        logging.getLogger().handlers.clear()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": "INFO",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file,
                    "formatter": "standard",
                    "level": "DEBUG",
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                },
            },
            "root": {"handlers": ["console", "file"], "level": "DEBUG"},
        }
    )
