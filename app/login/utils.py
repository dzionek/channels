from secrets import token_hex
from os import path, remove
from PIL import Image

from flask import render_template
from flask_login import current_user

from typing import Optional
from werkzeug.datastructures import FileStorage

from app.bcrypt.utils import hash_password, check_hashed_password

from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm

from app.models import db
from app.models.channel import Channel
from app.models.message import Message
from app.models.user import User, DEFAULT_PROFILE_PICTURE

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

def update_user(username: str, email: str) -> None:
    """Update the current user setting her/him the given username and email.
    Commit all the changes to database, including the change of the profile picture.

    Args:
        username: The new username of the current user.
        email: The new email of the current user.

    """
    current_user.username = username
    current_user.email = email
    db.session.commit()

def get_profile_picture_full_path(profile_picture_filename: str) -> str:
    """Get the full path of the profile picture from the given relative path.

    Args:
        profile_picture_filename: The relative path to the profile picture.

    Returns:
        The full path to the profile picture.

    """
    return path.join('app', 'static', 'img', 'profile_pictures', profile_picture_filename)

def remove_old_profile_picture() -> None:
    """Remove the profile picture of the current user."""
    if current_user.profile_picture != DEFAULT_PROFILE_PICTURE:
        old_profile_picture_path = get_profile_picture_full_path(current_user.profile_picture)
        remove(old_profile_picture_path)

def save_profile_picture(picture: FileStorage) -> str:
    """Save the given profile picture on the server and returns its relative path.
    The root directory is the one where all profile pictures are stored.
    The change is committed to the DB in update_user function.

    Args:
        picture: The profile picture to be saved.

    Returns:
        The relative path to the profile picture.

    """
    random_hex = token_hex(8)
    _, file_extension = path.splitext(picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = get_profile_picture_full_path(picture_filename)

    output_size = (125, 125)
    image = Image.open(picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename
