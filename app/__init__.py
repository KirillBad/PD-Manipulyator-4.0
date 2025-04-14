from logging.config import dictConfig

from flask import Flask

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": "app.log",
                "formatter": "default",
            }
        },
        "loggers": {"werkzeug": {"level": "ERROR", "handlers": ["file"]}},
        "root": {"level": "INFO", "handlers": ["file"]},
    }
)

app = Flask(__name__)
from app import routes  # noqa: E402, F401
