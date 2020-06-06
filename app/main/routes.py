from flask import request
from typing import Tuple

from .base import main
from .utils import *

"""
Routes for the main functionality of the app.
"""

@main.route('/add-channel', methods=['POST'])
def add_channel_ajax() -> Any:
    """Take POST form with the parameter 'channelName', check if it is a unique valid channel name.
    If it is valid, add it to database. Return JSON saying if adding a channel was successful.

    Returns:
        JSON response consisting of boolean 'success' attribute and optionally 'errorMessage'.

    Raises:
        ValueError: If channel_name is None.

    """
    channel_name = request.form.get('channelName')

    if channel_name is None:
        raise TypeError('Channel name must not be None.')
    else:
        channel_name = str(channel_name)

    if channel_has_invalid_name(channel_name):
        return jsonify({
            'success': False, 'errorMessage': f'You cannot create a channel of the given name: {channel_name}'
        })

    elif channel_already_exists(channel_name):
        return jsonify({'success': False, 'errorMessage': 'The channel already exists'})

    else:
        add_channel(channel_name)
        return jsonify({'success': True})

@main.route('/get-messages', methods=['POST'])
def get_messages_ajax() -> Any:
    """Take POST form with the parameter 'channelName' and return its messages in JSON format.

    Returns:
        JSON response consisting of all messages in this channel.

    Raises:
        ValueError: If channelName is None.

    """
    channel_name = request.form.get('channelName')

    if channel_name is None:
        raise ValueError('Channel name must not be None.')
    else:
        channel_name = str(channel_name)

    return get_messages(channel_name)

@main.route('/add-message', methods=['POST'])
def add_message_ajax() -> Tuple[str, int]:
    """Take POST form with the parameters 'messageContent' and 'channel'. Add the message to the channel
    and save it in the database.

    Returns:
        Empty response with 204 status code.

    Raises:
        ValueError: If message_content or channel is None.

    """
    message_content = request.form.get('messageContent')
    channel = request.form.get('channel')

    if message_content is None:
        raise ValueError('Message content must not be None.')
    elif channel is None:
        raise ValueError('Channel must not be None.')
    else:
        message_content, channel = str(message_content), str(channel)

    add_message(message_content, channel)

    return '', 204