from flask import Flask

from .config import configure_app
from . import models, main, login, sockets

"""
Module containing the app factory.
"""

def create_app() -> Flask:
    """Flask app factory initialising all its components.

    Returns:
        The created Flask application.
    """
    app = Flask(__name__)
    configure_app(app)

    models.init_app(app)
    main.init_app(app)
    login.init_app(app)
    sockets.init_app(app)

    return app