from flask import Flask
from .base import socket_io

def init_app(app: Flask) -> None:
    socket_io.init_app(app)