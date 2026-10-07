from __future__ import annotations

from flask import Flask
from flask_compress import Compress

from .bootstrap.runtime_warmup import start_runtime_warmup_tasks
from .dash import init_dash_app
from .env_configuration import EnvConfiguration
from .factory import create_flask_app
from .logging_config import setup_logging
from .middlewares import register_middlewares
from .routes import register_routes


def create_app() -> Flask:
    settings = EnvConfiguration.from_env()
    setup_logging()

    app = create_flask_app(settings=settings)
    with app.app_context():
        init_dash_app(app=app, settings=settings)
        Compress(app=app)

    register_routes(app=app, settings=settings)
    register_middlewares(app=app)

    start_runtime_warmup_tasks(app=app)

    return app
