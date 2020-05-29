from flask import Blueprint, jsonify, request
from .utils import channel_has_invalid_name, channel_already_exists, add_channel

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