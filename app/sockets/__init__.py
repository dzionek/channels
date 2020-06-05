from flask import Flask
from .base import socket_io

"""
Module containing Socket.IO initialization.
"""

def init_app(app: Flask) -> None:
    """Initialize Socket.IO in the app.

    Args:
        app: Flask application where Socket.IO should be initialized.
    """
    socket_io.init_app(app)