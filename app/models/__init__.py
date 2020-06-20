from flask import Flask

from .base import db

from .user import User
from .message import Message
from .channel import Channel
from .channel_allowlist import ChannelAllowList

"""
Module containing function which initialize database.
"""

def init_app(app: Flask) -> None:
    """Initialize database in the application.

    Args:
        app: Flask application the database should be initialized in.

    """
    db.init_app(app)
