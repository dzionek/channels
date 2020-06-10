from flask import Flask

from secret_config import DATABASE_URI, SECRET_KEY

"""
Module containing settings of the app.
"""

def configure_app(app: Flask) -> None:
    """Set the internal settings of the app.

    Args:
        app: Flask application to be configured.

    """
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = True