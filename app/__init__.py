from flask import Flask

from .config import configure_app
from . import models, main, login, sockets, bcrypt, login_manager

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
    bcrypt.init_app(app)
    login_manager.init_app(app)

    return app