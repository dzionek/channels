"""Test the main package"""

from datetime import datetime
from typing import Callable

from app import app
from app.models import db, User, Channel, Message, ChannelAllowList
from app.models.channel_allowlist import UserRole
from app.bcrypt.utils import hash_password

from tests.utils import login, decode_bytecode_single_quote
from tests.test_login import route_context


def channel_settings_context(func: Callable) -> Callable:
    """The decorator for the test of the routes for settings of a channel.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.

    """
    @route_context
    def wrapper(*args, **kwargs) -> None:
        """Wrapper of the decorator."""
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        db.session.add(User(
            username='testUsername2', password=hash_password('testPassword2'), email='test2@email.com'
        ))
        db.session.add(Channel(name='channel', password='password'))
        db.session.add(ChannelAllowList(channel_id=1, user_id=1))
        func(*args, **kwargs)

    return wrapper


class TestRoutes:

    @route_context
    def test_get_messages_ajax(self) -> None:
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        db.session.add(Channel(name='channel', password='password'))

        with app.test_client() as c:
            rv = c.post('/get-messages', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'messages' not in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            rv = c.post('/get-messages', data={'channelName': 'channel', 'counter': '1'}, follow_redirects=True)
            assert 'Fatal error' in str(rv.data)

            rv = c.post('/get-messages', data={'channelName': 'channel', 'counter': 'NotANumber'}, follow_redirects=True)
            assert 'Fatal error' in str(rv.data)

            rv = c.post('/get-messages', data={'channelName': 'channel', 'counter': '0'}, follow_redirects=True)
            assert 'Fatal error' not in str(rv.data)
            json = eval(rv.data.decode('utf8'))
            assert json['messages'] == []

            for _ in range(5):
                db.session.add(Message(content='_', channel_id=1, user_id=1, time=datetime.utcnow()))

            rv = c.post('/get-messages', data={'channelName': 'channel', 'counter': '3'}, follow_redirects=True)
            assert 'messages' in str(rv.data)
            json = eval(rv.data.decode('utf8'))
            assert len(json['messages']) == 3
            for content, user in [[message['content'], message['userName']] for message in json['messages']]:
                assert content == '_'
                assert user == 'testUsername'

            for _ in range(20):
                db.session.add(Message(content='&', channel_id=1, user_id=1, time=datetime.utcnow()))

            rv = c.post('/get-messages', data={'channelName': 'channel', 'counter': '25'}, follow_redirects=True)
            json = eval(rv.data.decode('utf8'))

            assert len([message['content'] for message in json['messages']]) == 20

            assert set([message['content'] for message in json['messages']]) == set('&')

    @route_context
    def test_get_initial_counter_ajax(self) -> None:
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        db.session.add(Channel(name='channel', password='password'))

        with app.test_client() as c:
            rv = c.post('/get-messages', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'counter' not in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            rv = c.post('/initial-counter', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'counter' in str(rv.data)
            json = eval(rv.data.decode('utf8'))
            assert json['counter'] == 0

            for _ in range(20):
                db.session.add(Message(content='&', channel_id=1, user_id=1, time=datetime.utcnow()))

            rv = c.post('/initial-counter', data={'channelName': 'channel'}, follow_redirects=True)
            json = eval(rv.data.decode('utf8'))
            assert json['counter'] == 20

    @channel_settings_context
    def test_leave_channel(self) -> None:
        db.session.add(ChannelAllowList(channel_id=1, user_id=2))

        with app.test_client() as c:
            rv = c.post('/leave-channel', data={'channel': 'channel'}, follow_redirects=True)
            assert 'the channel' not in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            rv = c.post('/leave-channel', data={'channel': 'channel'}, follow_redirects=True)
            assert 'the channel' in str(rv.data)
            assert 'the last user' not in str(rv.data)

            assert len(ChannelAllowList.query.all()) == 1

        with app.test_client() as c:
            rv = login(c, 'test2@email.com', 'testPassword2')
            assert 'Log out' in str(rv.data)

            rv = c.post('/leave-channel', data={'channel': 'channel'}, follow_redirects=True)
            assert 'the channel' in str(rv.data)
            assert 'the last user' in str(rv.data)

            assert not ChannelAllowList.query.all()

    @route_context
    def test_is_admin_ajax(self) -> None:
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        db.session.add(Channel(name='channel', password='password'))
        db.session.add(ChannelAllowList(channel_id=1, user_id=1))

        with app.test_client() as c:
            rv = c.post('/is-admin', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'response' not in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            # User is not admin of the channel.
            rv = c.post('/is-admin', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'response' in str(rv.data)

            json = eval(rv.data.decode('utf8').replace('false', 'False').replace('true', 'True'))
            assert not json['response']

            ChannelAllowList.query.first().user_role = UserRole.ADMIN.value

            # User is admin of the channel
            rv = c.post('/is-admin', data={'channelName': 'channel'}, follow_redirects=True)
            assert 'response' in str(rv.data)

            json = eval(rv.data.decode('utf8').replace('false', 'False').replace('true', 'True'))
            assert json['response']

            # No channel given in the form
            rv = c.post('/is-admin', follow_redirects=True)
            assert 'response' in str(rv.data)

            json = eval(rv.data.decode('utf8').replace('false', 'False').replace('true', 'True'))
            assert not json['response']

            # Channel given in the form doesn't exist
            rv = c.post('/is-admin', data={'channelName': 'channel_second'}, follow_redirects=True)
            assert 'response' in str(rv.data)

            json = eval(rv.data.decode('utf8').replace('false', 'False').replace('true', 'True'))
            assert not json['response']

    @route_context
    def test_channel_settings(self) -> None:
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        db.session.add(Channel(name='channel', password='password'))
        db.session.add(ChannelAllowList(channel_id=1, user_id=1))

        with app.test_client() as c:
            rv = c.get('/channel/channel', follow_redirects=True)
            assert 'Please log in to access this page' in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            rv = c.get('/channel/channel', follow_redirects=True)
            assert 'Number of users:' not in str(rv.data)
            assert "you don't have necessary permission" in decode_bytecode_single_quote(rv.data)

            ChannelAllowList.query.first().user_role = UserRole.ADMIN.value

            rv = c.get('/channel/channel', follow_redirects=True)
            assert 'Number of users:' in str(rv.data)

            rv = c.get('/channel/channel_second', follow_redirects=True)
            assert 'Number of users:' not in str(rv.data)
            assert "channel doesn't exist" in decode_bytecode_single_quote(rv.data)

    @channel_settings_context
    def test_make_admin(self) -> None:
        with app.test_client() as c:
            rv = c.post('/make-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert 'Please log in to access this page' in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            # The caller is not admin.
            rv = c.post('/make-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" in decode_bytecode_single_quote(rv.data)

            ChannelAllowList.query.filter_by(user_id=1).first().user_role = UserRole.ADMIN.value

            # The caller is admin but the nominated user is not allowed to be in the channel.
            rv = c.post('/make-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" in decode_bytecode_single_quote(rv.data)

            # The caller is admin and the nominated user can see the channel
            db.session.add(ChannelAllowList(channel_id=1, user_id=2))
            rv = c.post('/make-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" not in decode_bytecode_single_quote(rv.data)
            assert ChannelAllowList.query.filter_by(user_id=2).first().user_role == UserRole.ADMIN.value

    @channel_settings_context
    def test_revoke_admin(self) -> None:
        with app.test_client() as c:
            rv = c.post('/revoke-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert 'Please log in to access this page' in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            # The caller is not admin.
            rv = c.post('/revoke-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" in decode_bytecode_single_quote(rv.data)

            ChannelAllowList.query.filter_by(user_id=1).first().user_role = UserRole.ADMIN.value

            # The caller is admin but the nominated user is not allowed to be in the channel.
            rv = c.post('/revoke-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" in decode_bytecode_single_quote(rv.data)

            # The caller is admin, the nominated user can see the channel
            db.session.add(ChannelAllowList(channel_id=1, user_id=2, user_role=UserRole.ADMIN.value))
            rv = c.post('/revoke-admin', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "It wasn't possible to modify the role of the given user" not in decode_bytecode_single_quote(rv.data)
            assert ChannelAllowList.query.filter_by(user_id=2).first().user_role == UserRole.NORMAL_USER.value

    @channel_settings_context
    def test_remove_user(self) -> None:
        db.session.add(ChannelAllowList(channel_id=1, user_id=2, user_role=UserRole.ADMIN.value))
        with app.test_client() as c:
            rv = c.post('/remove-user', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert 'Please log in to access this page' in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            # The caller is not admin.
            rv = c.post('/remove-user', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "The user can't be removed" in decode_bytecode_single_quote(rv.data)

            # The caller is admin but so is the second user.
            ChannelAllowList.query.filter_by(user_id=1).first().user_role = UserRole.ADMIN.value
            rv = c.post('/remove-user', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "The user can't be removed" in decode_bytecode_single_quote(rv.data)
            assert ChannelAllowList.query.filter_by(user_id=2).first()

            # The caller is admin but the second user is not.
            ChannelAllowList.query.filter_by(user_id=2).first().user_role = UserRole.NORMAL_USER.value
            rv = c.post('/remove-user', data={'channel_id': 1, 'user': 2}, follow_redirects=True)
            assert "The user can't be removed" not in decode_bytecode_single_quote(rv.data)
            assert not ChannelAllowList.query.filter_by(user_id=2).first()
