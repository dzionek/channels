from flask import Blueprint, request

from .utils import *

main = Blueprint('main', __name__)

@main.route('/add-channel', methods=['POST'])
def add_channel_ajax():
    channel_name = request.form.get('channelName')
    if channel_has_invalid_name(channel_name):
        return jsonify({'success': False, 'errorMessage': f'You cannot create a channel of the given name: {channel_name}'})
    elif channel_already_exists(channel_name):
        return jsonify({'success': False, 'errorMessage': 'The channel already exists'})
    else:
        add_channel(channel_name)
        return jsonify({'success': True})

@main.route('/get-messages', methods=['POST'])
def get_messages_ajax():
    channel_name = request.form.get('channelName')
    return get_messages(channel_name)

@main.route('/add-message', methods=['POST'])
def add_message_ajax():
    message_content = request.form.get('messageContent')
    channel = request.form.get('channel')
    add_message(message_content, channel)
    return '', 204