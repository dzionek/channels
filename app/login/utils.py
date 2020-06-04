from flask import session, render_template
from app.models.base import db
from app.models.user import User
from app.models.channel import Channel
from app.models.message import Message

def log_in(request_form):
    username = request_form.get('username')
    session['username'] = username
    return set_up_app()

def is_logged():
    if not session.get('username'):
        return False
    elif not isinstance(session['username'], str):
        raise TypeError('Username is not a string')
    else:
        return True

def set_up_app():
    username = session['username']
    if not User.query.filter_by(username=username).first():
        db.session.add(User(username=username))
        db.session.commit()

    channels = Channel.query.all()
    messages = Message.query.all()

    return render_template(
        'app.html', username=username, channels=channels, messages=messages
    )