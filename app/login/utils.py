from flask import session, render_template

from app.models.channel import Channel
from app.models.message import Message

"""
Utility functions for login routes.
"""

def log_in(username: str) -> str:
    """Log in user of the given username.

    Args:
        username: Name of the user.

    Returns:
        Template of the main part of the app.

    """
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

    channels = Channel.query.all()
    messages = Message.query.all()

    return render_template(
        'app.html', username=username, channels=channels, messages=messages
    )
