from .routes import main
from flask import Flask

def init_app(app: Flask) -> None:
    app.register_blueprint(main)