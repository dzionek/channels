from flask_login import UserMixin

from .base import db

"""
Module containing the class of the user model.
"""

DEFAULT_PROFILE_PICTURE = 'default.png'

class User(db.Model, UserMixin):
    """Model of the user of the app.

    Fields:
        id (int): Primary key of the user.\n
        username (str): Name of the user.\n
        email (str): Email of the user.\n
        password (str): Password of the user.\n
        profile_picture (str): Relative path to the profile picture of the user.

    Relationships:
        messages: All messages the user sent. One to many relationship with Message model.\n
        allowed_channels: All channels the user is allowed to see.

    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default=DEFAULT_PROFILE_PICTURE)

    messages = db.relationship('Message', backref='user', lazy=True)
    allowed_channels = db.relationship('ChannelAllowList', backref='user', lazy=True)

    def __repr__(self) -> str:
        """Get representation of a user.

        Returns:
            String representation of a user.

        """
        return f"User(name='{self.username}')"
