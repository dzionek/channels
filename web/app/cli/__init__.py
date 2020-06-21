from .bp import cli_bp
from flask import Flask

"""
Module containing the cli blueprint registration.
"""

def init_app(app: Flask) -> None:
    """Initialize cli blueprint in the app.

    Args:
        app: Flask application where cli blueprint should be initialized in.

    """
    app.register_blueprint(cli_bp)
