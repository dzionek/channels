from flask import request
from typing import Tuple

from .base import main
from .utils import *

"""
Routes for the main functionality of the app.
"""

@main.route('/add-channel', methods=['POST'])
def add_channel_ajax() -> Response:
    """Take POST form with the parameter 'channelName', check if it is a unique valid channel name.
    If it is valid, add it to database. Return JSON saying if adding a channel was successful.

    Returns:
        JSON response consisting of boolean 'success' attribute and optionally 'errorMessage'.

    """
    channel_name = request.form.get('channelName')

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
def get_messages_ajax() -> Response:
    """Take POST form with the parameter 'channelName' and return its messages in JSON format.

    Returns:
        JSON response consisting of all messages in this channel.

    """
    channel_name = request.form.get('channelName')
    return get_messages(channel_name)

@main.route('/add-message', methods=['POST'])
def add_message_ajax() -> Tuple[str, int]:
    """Take POST form with the parameters 'messageContent' and 'channel'. Add the message to the channel
    and save it in the database.

    Returns:
        Empty response with 204 status code.

    """
    message_content = request.form.get('messageContent')
    channel = request.form.get('channel')

    add_message(message_content, channel)

    return '', 204