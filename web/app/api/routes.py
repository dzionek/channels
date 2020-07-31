"""
All routes of the "API" blueprint.
"""

from flask import render_template, request, abort, jsonify
from flask_login import login_required, current_user
from app.models import User, Channel
from app.schemas import ChannelSchema

from .base import api

@api.route('/api/settings')
@login_required
def settings() -> str:
    """Generate API settings page for the user with

    Returns:
        The API settings page with the generated token.

    """
    token = current_user.generate_api_token()
    return render_template('settings-api.html', token=token)

@api.route('/api/channels', methods=['POST'])
def show_user():
    token = request.form.get('token')
    if not token:
        abort(404, description="Token not found.")

    user = User.verify_api_token(token)
    if not user:
        abort(403, description="The token is either invalid or expired.")
    else:
        channels = [
            Channel.query.get(allowed_record.channel_id)
            for allowed_record in user.allowed_channels
        ]
        channel_schema = ChannelSchema()
        return jsonify(channel_schema.dump(channels, many=True))
