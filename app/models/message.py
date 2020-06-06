from .base import db

"""
Module containing class of the message model.
"""

class Message(db.Model):
    """Model of the message users sent to channels.

    Fields:
        id: Primary key of the message.\n
        content: Content of the message.\n
        user_id: ID of the user who sent the message.\n
        time: Time when the message was sent.\n
        channel_id: Id of the channel the message was sent to.

    """
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
