"""
This package implements Socket.IO and its methods within the application.
This particular module contains Socket.IO initialization.
"""

from flask import Flask
from .base import socket_io

def init_app(app: Flask) -> None:
    """Initialize Socket.IO in the app.

    Args:
        app: Flask application where Socket.IO should be initialized.

    """
    socket_io.init_app(app)
