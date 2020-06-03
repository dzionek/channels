import re
from flask import jsonify, session
from src.models.base import db
from src.models.channel import Channel
from src.models.message import Message
from src.models.user import User
from ..sockets.sockets import announce_channel, announce_message

VALID_PATTERN = re.compile(r'[A-Za-z0-9 \-_]+')

def channel_has_invalid_name(channel_name):

    if not channel_name:
        return True
    else:
        return not(bool(re.fullmatch(VALID_PATTERN, channel_name))) \
               or channel_name.startswith(' ') \
               or channel_name.endswith(' ')


def channel_already_exists(channel_name):
    channel = Channel.query.filter_by(name=channel_name).first()
    return bool(channel)

def add_channel(channel_name):
    db.session.add(Channel(name=channel_name))
    db.session.commit()
    announce_channel(channel_name)

def get_messages(channel_name):
    channel = Channel.query.filter_by(name=channel_name).first()
    messages = Message.query.filter_by(channel_id=channel.id).all()
    messages_response = [
        {
            'user': User.query.filter_by(id=message.user_id).first().username,
            'content': message.content,
            'time': message.time
        }
        for message in messages
    ]
    return jsonify({'messages': messages_response})

def add_message(message_content, channel):
    username = session['username']
    user_id = User.query.filter_by(username=username).first().id

    from datetime import datetime
    time = datetime.now()

    channel_id = Channel.query.filter_by(name=channel).first().id

    db.session.add(Message(
        content=message_content, user_id=user_id, time=time, channel_id=channel_id
    ))

    db.session.commit()
    announce_message(username, str(time), channel, message_content)