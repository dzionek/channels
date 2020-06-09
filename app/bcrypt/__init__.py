from flask import Flask
from .base import bcrypt

"""
Module containing Bcrypt initialization.
"""

def init_app(app: Flask) -> None:
    """Initialize Bcrypt in the app.

    Args:
        app: Flask application where Bcrypt should be work in.

    """
    bcrypt.init_app(app)