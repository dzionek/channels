import re
from flask import jsonify
from src.models.base import db
from src.models.channel import Channel
from src.models.message import Message

VALID_PATTERN = re.compile(r'[A-Za-z0-9 \-_]+')

def channel_has_invalid_name(channel_name: str) -> bool:

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

def get_messages(channel_name):
    channel = Channel.query.filter_by(name=channel_name).first()
    messages = Message.query.filter_by(channel_id=channel.id).all()
    messages_jsonable = [message.content for message in messages]
    return jsonify({'messages': messages_jsonable})