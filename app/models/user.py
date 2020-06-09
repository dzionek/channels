from flask_login import UserMixin

from .base import db

class User(db.Model, UserMixin):
    """Model of the user of the app.

    Fields:
        id: Primary key of the user.\n
        username: Name of the user.\n

    Relationships:
        messages: All messages the user sent. One to many relationship with Message model.

    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self) -> str:
        """Get representation of a user.

        Returns:
            String representation of a user.

        """
        return f"User(name='{self.username}')"