from datetime import datetime
from typing import Any
from werkzeug.wrappers import Response

from flask import jsonify, url_for, redirect
from flask_login import current_user

from app.models import db, ChannelAllowList, Message, User, Channel
from app.models.channel_allowlist import UserRole

from app.sockets.sockets import announce_channel, announce_message
from app.bcrypt.utils import hash_password

from app.forms.channel import UpdateChannelForm, AddChannelForm, JoinChannelForm
"""
Utility functions for main routes.
"""

def add_channel(channel_name: str) -> None:
    """Add channel to the database and emit it with Socket.IO.

    Args:
        channel_name: Name of the channel to be added.

    """
    db.session.add(Channel(name=channel_name))
    db.session.commit()
    announce_channel(channel_name)

def pretty_time(full_time: datetime) -> str:
    """Take datetime object and get its string of the form YYYY-MM-DD HH:MM.

    Args:
        full_time: DateTime object which pretty form the function should return.

    Returns:
        String YYYY-MM-DD HH:MM.

    """
    full_time_str = str(full_time)
    length_boundary = len('2020-01-01 00:00')
    return full_time_str[:length_boundary]

def get_messages(channel_name: str, counter: int) -> Any:
    """Get the messages of the given channel and return them in JSON format.
    The function supports dynamic loading and will return only a specified number of messages.
    The last message to be loaded is given by the argument "counter".

    Args:
        channel_name: Name of the channel which messages the function should look for.
        counter: Id of the last message to be displayed.

    Returns:
        JSON response with all data about messages of the channel.

    """
    num_messages_loaded_at_once = 20

    channel = Channel.query.filter_by(name=channel_name).first()
    messages = channel.messages

    messages_response = [
        {
            'userName': User.query.filter_by(id=message.user_id).first().username,
            'userPicture': f"{url_for('static', filename='img/profile_pictures')}/"
                           f"{ User.query.filter_by(id=message.user_id).first().profile_picture }",
            'content': message.content,
            'time': pretty_time(message.time)
        }
        for message in messages[max(counter - num_messages_loaded_at_once, 0):counter]
    ]
    return jsonify({'messages': messages_response})

def add_message(message_content: str, channel: str) -> None:
    """Add the given message to the given channel in database. Emit the message with Socket.IO
    after adding it.

    Args:
        message_content: Content of the message to be added.
        channel: Channel the message should be added to.

    """
    username = current_user.username
    user_id = current_user.id
    user_picture = f"{url_for('static', filename='img/profile_pictures')}/{ current_user.profile_picture }"

    full_time = datetime.now()

    channel_id = Channel.query.filter_by(name=channel).first().id

    db.session.add(Message(
        content=message_content, user_id=user_id, time=full_time, channel_id=channel_id
    ))

    db.session.commit()
    announce_message(username, user_picture, pretty_time(full_time), channel, message_content)

def is_valid_channel(channel: None, form_password: str) -> bool:
    """Check if the given user exists and then check if the password provided in the login form
    matches this user's password in the database.

    Args:
        channel: None or the user in the database.
        form_password: The filled login form.

    Returns:
        True if the user is valid, false otherwise.

    """
    # if isinstance(channel, User):
    #     return check_hashed_password(channel.password, form_password)
    # else:
    #     return False
    pass

def process_add_channel_form(form: AddChannelForm) -> Response:
    """Get the validated form to add a channel. Hash the given password of the channel.
    Set the current user admin role on this channel. Save all of that in the database.

    Args:
        form: The filled form to add a channel.

    """
    hashed_password = hash_password(form.password.data)

    db.session.add(Channel(
        name=form.name.data, password=hashed_password
    ))

    channel_id = Channel.query.filter_by(password=hashed_password).first().id

    db.session.add(ChannelAllowList(
        channel_id=channel_id, user_id=current_user.id, user_role=UserRole.ADMIN.value
    ))

    db.session.commit()

    return redirect(url_for('main.setup_app'))

def process_join_channel(form: JoinChannelForm):
    # channel = User.query.filter_by(email=form.email.data).first()
    # if is_valid_user(user, form):
    #     login_user(user=user, remember=form.remember)
    #     next_page = request.args.get('next')
    #     return redirect(next_page) if next_page else redirect(url_for('main.setup_app'))
    # else:
    #     flash('Login Unsuccessful. Incorrect email or password', 'danger')
    pass

def process_update_channel_form(form: UpdateChannelForm):
    pass
