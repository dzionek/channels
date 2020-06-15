from flask import request, render_template
from typing import Tuple

from .base import main
from .utils import *

"""
Routes for the main functionality of the app.
"""

@main.route('/app')
def setup_app() -> str:
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

@main.route('/add-channel', methods=['POST'])
def add_channel_ajax() -> Any:
    """Take POST form with the parameter 'channelName' and add the channel to database."""
    channel_name = request.form.get('channelName')
    add_channel(channel_name)

@main.route('/get-messages', methods=['POST'])
def get_messages_ajax() -> Any:
    """Take POST form with the parameter 'channelName' and return its messages in JSON format.

    Returns:
        JSON response consisting of all messages in this channel.

    Raises:
        ValueError: If channelName is None.

    """
    channel_name = request.form.get('channelName')
    counter = request.form.get('counter')

    if channel_name is None or counter is None:
        raise ValueError('Channel name and counter must not be None.')
    else:
        channel_name = str(channel_name)
        counter = int(counter)

    return get_messages(channel_name, counter)

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

@main.route('/initial-counter', methods=['POST'])
def get_initial_counter_ajax() -> Any:
    """Get the initial counter of the channel given in the form.
    The initial counter is the id of the last message to be loaded dynamically.

    Returns:
        The initial counter of the channel.

    """
    channel_name = request.form.get('channelName')
    channel = Channel.query.filter_by(name=channel_name).first()

    return jsonify({
        'counter': len(channel.messages)
    })