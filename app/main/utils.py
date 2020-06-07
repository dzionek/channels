import re
from flask import jsonify, session
from datetime import datetime
from typing import Any

from app.models.base import db
from app.models.channel import Channel
from app.models.message import Message
from app.models.user import User
from ..sockets.sockets import announce_channel, announce_message

"""
Utility functions for main routes.
"""

valid_pattern = re.compile(r'[A-Za-z0-9 \-_]+')

def channel_has_invalid_name(channel_name: str) -> bool:
    """Check if the channel has invalid name. Its name is invalid if either it is empty,
    has trailing or leading spaces, or violates the `valid_pattern` regex.

    Args:
        channel_name: Name of the channel to be checked.

    Returns:
        True if it has invalid name, False otherwise.

    """

    if not channel_name:
        return True
    else:
        return not(bool(re.fullmatch(valid_pattern, channel_name))) \
               or channel_name.startswith(' ') \
               or channel_name.endswith(' ')


def channel_already_exists(channel_name: str) -> bool:
    """Check if the channel already exists in the database.

    Args:
        channel_name: Name of the channel to be checked.

    Returns:
        True if it already exists, false otherwise.

    """
    channel = Channel.query.filter_by(name=channel_name).first()
    return bool(channel)

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

def get_messages(channel_name: str) -> Any:
    """Get messages of the given channel and return them in JSON format.

    Args:
        channel_name: Name of the channel which messages the function should look for.

    Returns:
        JSON response with all data about messages of the channel.

    """
    channel = Channel.query.filter_by(name=channel_name).first()
    messages = Message.query.filter_by(channel_id=channel.id).all()
    messages_response = [
        {
            'user': User.query.filter_by(id=message.user_id).first().username,
            'content': message.content,
            'time': pretty_time(message.time)
        }
        for message in messages
    ]
    return jsonify({'messages': messages_response})

def add_message(message_content: str, channel: str) -> None:
    """Add the given message to the given channel in database. Emit the message with Socket.IO
    after adding it.

    Args:
        message_content: Content of the message to be added.
        channel: Channel the message should be added to.

    """
    username = session['username']
    user_id = User.query.filter_by(username=username).first().id

    full_time = datetime.now()

    channel_id = Channel.query.filter_by(name=channel).first().id

    db.session.add(Message(
        content=message_content, user_id=user_id, time=full_time, channel_id=channel_id
    ))

    db.session.commit()
    announce_message(username, pretty_time(full_time), channel, message_content)