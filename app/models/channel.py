from .base import db

"""
Module containing class of the channel model.
"""

class Channel(db.Model):
    """Model of the channel for storing messages.

    Fields:
        id (int): Primary key of the channel.\n
        name (str): Name of the channel. Cannot be longer than 30 characters.

    Relationships:
        messages: All messages the channel has. One to many relationship with Message model.
    """
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    messages = db.relationship('Message', backref='channel', lazy=True)