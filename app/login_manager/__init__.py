from flask import Flask

from .base import login_manager
from app.models.user import User

"""
Module containing Login Manager initialization.
"""

def init_app(app: Flask) -> None:
    """Initialize Login Manager in the app.

    Args:
        app: Flask application where Login Manager should be work in.

    """
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)