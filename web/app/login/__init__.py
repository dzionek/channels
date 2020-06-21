from .routes import login
from flask import Flask

"""
Module containing the 'login' routes blueprint registration.
"""

def init_app(app: Flask) -> None:
    """Initialize login routes with their functionality in the application.

    Args:
        app: Flask application where routes should be initialized in.

    """
    app.register_blueprint(login)