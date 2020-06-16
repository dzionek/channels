from typing import Tuple, Any

from flask import request, render_template, jsonify
from flask_login import current_user, login_required

from .base import main
from .utils import add_channel, get_messages, add_message, process_add_channel_form, process_update_channel_form,\
    process_join_channel_form

from app.models import Channel, ChannelAllowList

from app.forms.channel import AddChannelForm, UpdateChannelForm, JoinChannelForm

"""
Routes for the main functionality of the app.
"""

@main.route('/app', methods=['GET', 'POST'])
@login_required
def setup_app() -> str:
    """Get username, channels and messages from database and render the main app
    template with them.

    Returns:
        Rendered template of the main app.

    """
    add_channel_form = AddChannelForm()
    join_channel_form = JoinChannelForm()
    update_channel_form = UpdateChannelForm()

    add_channel_form_invalid = False
    join_channel_form_invalid = False
    update_channel_form_invalid = False

    if add_channel_form.submit_add.data:
        if add_channel_form.validate_on_submit():
            process_add_channel_form(add_channel_form)
        else:
            add_channel_form_invalid = True

    elif join_channel_form.submit_join.data:
        if join_channel_form.validate_on_submit():
            process_join_channel_form(join_channel_form)
        else:
            join_channel_form_invalid = True

    elif update_channel_form.submit_update.data:
        if update_channel_form.validate_on_submit():
            process_update_channel_form(update_channel_form)
        else:
            update_channel_form_invalid = True

    allowed_channels = ChannelAllowList.query.filter_by(user_id=current_user.id).all()
    channels = [allowed_channel.channel for allowed_channel in allowed_channels]

    return render_template(
        'app.html', username=current_user, channels=channels,

        add_channel_form=add_channel_form,
        join_channel_form=join_channel_form,
        update_channel_form=update_channel_form,

        add_channel_form_invalid=add_channel_form_invalid,
        join_channel_form_invalid=join_channel_form_invalid,
        update_channel_form_invalid=update_channel_form_invalid
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
