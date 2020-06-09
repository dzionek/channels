from flask import Flask

from .base import login_manager
from app.models.user import User

"""
Module containing Login Manager initialization with user loading.
"""

def init_app(app: Flask) -> None:
    """Initialize Login Manager in the app.

    Args:
        app: Flask application where Login Manager should be work in.

    """
    login_manager.init_app(app)
    login_manager.login_view = 'login.index'
    login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Let the login manager load the user of the given id.

    Args:
        user_id: Id of the user to be loaded in

    Returns:
        The loaded user.

    """
    user: User = User.query.get(user_id)
    return user
