from flask import session, render_template
from werkzeug.datastructures import ImmutableMultiDict

from app.models.base import db
from app.models.user import User
from app.models.channel import Channel
from app.models.message import Message

"""
Utility functions for login routes.
"""

def log_in(request_form: ImmutableMultiDict) -> str:
    """Log in user whose username was provided in the given request_form.

    Args:
        request_form: HTML form with get value with username.

    Returns:
        Template of the main part of the app.

    """
    username = request_form.get('username')
    session['username'] = username
    return set_up_app()

def is_logged() -> bool:
    """Check if the user is already logged in by checking if username session value exists.

    Returns:
        True if the user is logged in, False otherwise.

    """
    return session.get('username') is not None

def set_up_app() -> str:
    """Get username, channels and messages from database and render the main app
    template with them.

    Returns:
        Rendered template of the main app.
    """
    username = session['username']
    if not User.query.filter_by(username=username).first():
        db.session.add(User(username=username))
        db.session.commit()

    channels = Channel.query.all()
    messages = Message.query.all()

    return render_template(
        'app.html', username=username, channels=channels, messages=messages
    )