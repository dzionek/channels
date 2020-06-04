from secrets import DATABASE_URI, SECRET_KEY
from flask import Flask

def configure_app(app: Flask) -> None:
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.debug = True