"""Test the API package."""

from app import app
from app.bcrypt.utils import hash_password
from app.models import db, User

from tests.test_login import route_context
from tests.utils import login


class TestRoutes:

    @route_context
    def test_settings(self) -> None:
        db.session.add(User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        ))
        with app.test_client() as c:
            rv = c.get('/api-settings', follow_redirects=True)
            assert 'Please log in to access this page' in str(rv.data)

            rv = login(c, 'test@email.com', 'testPassword')
            assert 'Log out' in str(rv.data)

            rv = c.get('/api-settings', follow_redirects=True)
            assert 'API settings will be here with token' in str(rv.data)
