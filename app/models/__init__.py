from flask import Flask
from .base import db

"""
Module containing function which initialize database.
"""

def init_app(app: Flask) -> None:
    """Initialize database in the application. Create all its models.

    Args:
        app: Flask application the database should be initialized in.

    """
    db.init_app(app)
    with app.app_context():
        db.create_all()