from flask import Flask
from .config import configure_app

def create_app():
    """
    Flask app factory, initialising all its components.
    """
    from . import models, main, login, sockets
    app = Flask(__name__)
    configure_app(app)
    models.init_app(app)
    main.init_app(app)
    login.init_app(app)
    sockets.init_app(app)
    return app