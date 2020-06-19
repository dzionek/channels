from typing import Tuple, Any, Optional

from flask import request, render_template, jsonify, flash, redirect, url_for, Markup
from flask_login import current_user, login_required

from .base import main
from .utils import add_channel, get_messages, add_message, process_add_channel_form, process_update_channel_form, \
    process_join_channel_form, get_number_of_channels_users, get_number_of_channels_messages, get_channels_users, \
    admin_invalid, is_admin, admin_manager, check_channel_settings_form

from app.models import db, Channel, ChannelAllowList, User
from app.models.channel_allowlist import UserRole

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
@login_required
def add_channel_ajax() -> Any:
    """Take POST form with the parameter 'channelName' and add the channel to database."""
    channel_name = request.form.get('channelName')
    add_channel(channel_name)

@main.route('/get-messages', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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

@main.route('/leave-channel', methods=['POST'])
@login_required
def leave_channel():
    channel_name = request.form.get("channel")
    channel_id = Channel.query.filter_by(name=channel_name).first().id

    leave_msg = f'You have successfully leaved the channel "{channel_name}!"'

    (db.session.query(ChannelAllowList).filter(ChannelAllowList.user_id == current_user.id)
                                       .filter(ChannelAllowList.channel_id == channel_id)
                                       .delete())

    if not ChannelAllowList.query.filter_by(channel_id=channel_id).first():
        db.session.delete(Channel.query.filter_by(id=channel_id).first())
        leave_msg += '</br>Since you have been the last user, the channel has been deleted.'

    db.session.commit()
    flash(Markup(leave_msg), 'success')
    return redirect(url_for('main.setup_app'))

def no_channel() -> str:
    flash("The channel doesn't exist or you don't have necessary permission.", 'danger')
    return redirect(url_for('main.setup_app'))

@main.route('/is-admin', methods=['POST'])
def is_admin_ajax():
    channel_name = request.form.get('channelName')
    if not channel_name:
        return jsonify({'response': False})

    channel = Channel.query.filter_by(name=channel_name).first()

    if not channel:
        return jsonify({'response': False})

    return jsonify({'response': is_admin(channel, current_user)})

@main.route('/channel/<string:channel_name>', methods=['GET'])
@login_required
def channel_settings(channel_name: str) -> str:
    channel = Channel.query.filter_by(name=channel_name).first()

    if not channel:
        return no_channel()

    channel_permit = (ChannelAllowList.query.filter_by(user_id=current_user.id)
                                            .filter_by(channel_id=channel.id).first())

    if channel_permit and channel_permit.user_role == UserRole.ADMIN.value:

        num_users = get_number_of_channels_users(channel)
        num_messages = get_number_of_channels_messages(channel)
        users = get_channels_users(channel)

        only_admins = all([is_admin(channel, user) for user in users])
        user_tuples = [(user, is_admin(channel, user)) for user in users]

        return render_template(
            'settings-channel.html',
            channel=channel, num_users=num_users, num_messages=num_messages, user_tuples=user_tuples,
            only_admins=only_admins
        )

    else:
        return no_channel()

@main.route('/make-admin', methods=['POST'])
@login_required
def make_admin():
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user')
    return admin_manager(command='make', channel_id=channel_id, user_id=user_id)

@main.route('/revoke-admin', methods=['POST'])
@login_required
def revoke_admin():
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user')
    return admin_manager(command='revoke', channel_id=channel_id, user_id=user_id)

@main.route('/remove-user', methods=['POST'])
@login_required
def remove_user() -> str:
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user')

    checked_value = check_channel_settings_form(channel_id, user_id)

    if not checked_value:
        flash("The user can't be removed.", 'danger')
        return redirect(url_for('main.setup_app'))
    else:
        channel, user = checked_value

    allow_record = (ChannelAllowList.query.filter_by(channel_id=channel.id)
                                          .filter_by(user_id=user.id).first())

    db.session.delete(allow_record)

    db.session.commit()
    flash(f"The user {user.username} has been removed from channel {channel.name}.", 'success')
    return redirect(f"channel/{channel.name}")
