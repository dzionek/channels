from .routes import main
from flask import Flask

"""
Module containing the 'main' routes blueprint registration.
"""

def init_app(app: Flask) -> None:
    """Initialize main routes with their functionality in the application.

    Args:
        app: Flask application where routes should be initialized in.

    """
    app.register_blueprint(main)