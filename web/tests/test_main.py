"""Test the main package"""

from datetime import datetime

from app import app
from app.models import db, User, Channel, Message
from app.bcrypt.utils import hash_password

from tests.utils import login
from tests.test_login import route_context

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