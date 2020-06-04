from flask import Flask
from .base import db

def init_app(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()