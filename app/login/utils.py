from flask import render_template
from flask_login import current_user
from typing import Optional

from app.bcrypt.utils import hash_password, check_hashed_password

from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm

from app.models import db
from app.models.channel import Channel
from app.models.message import Message
from app.models.user import User

"""
Utility functions for login routes.
"""

def set_up_app() -> str:
    """Get username, channels and messages from database and render the main app
    template with them.

    Returns:
        Rendered template of the main app.

    """
    channels = Channel.query.all()
    messages = Message.query.all()

    return render_template(
        'app.html', username=current_user, channels=channels, messages=messages
    )


def add_user(form: RegistrationForm) -> None:
    """Add user (whose data is given in the registration form) to the database.

    Args:
        form: The filled registration form.

    """
    hashed_password = hash_password(form.password.data)
    db.session.add(User(
        username=form.username.data, email=form.email.data, password=hashed_password
    ))
    db.session.commit()


def is_valid_user(user: Optional[User], form: LoginForm) -> bool:
    """Check if the given user exists and then check if the password provided in the login form
    matches this user's password in the database.

    Args:
        user: None or the user in the database.
        form: The filled login form.

    Returns:
        True if the user is valid, false otherwise.

    """
    if isinstance(user, User):
        return check_hashed_password(user.password, form.password.data)
    else:
        return False

def get_number_of_all_messages() -> int:
    """Get the number of all channels that the given user has sent.

    Returns:
        The number of all messages of the user.

    """
    number_of_all_messages: int = Message.query.filter_by(user_id=current_user.id).count()
    return number_of_all_messages

def get_number_of_all_channels() -> int:
    """Get the number of all channels.

    Returns:
        The number of all channels.

    """
    number_of_all_channels: int = Channel.query.count()
    return number_of_all_channels