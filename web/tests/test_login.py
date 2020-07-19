"""Test the login package."""

import pytest
from datetime import datetime
import os
from PIL import Image

import app.login.utils as u
from tests.utils import login

from app import app
from app.models import db, User, Message, Channel, ChannelAllowList

from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm

from app.bcrypt.utils import check_hashed_password, hash_password

class TestUtils:

    @pytest.fixture
    def test_user_1(self) -> User:
        return User(
            username='testUsername', password=hash_password('testPassword'), email='test@email.com'
        )

    @pytest.fixture
    def test_user_2(self) -> User:
        return User(
            username='testUsername2', password=hash_password('testPassword2'), email='test2@email.com'
        )

    @pytest.fixture
    def test_channel(self) -> Channel:
        return Channel(name='testChannel', password='testPassword')

    def test_add_user(self) -> None:
        with app.app_context():
            db.drop_all()
            db.create_all()

            username = 'testUsername'
            password = 'testPassword'
            email = 'test@email.com'

            with app.test_request_context():
                form = RegistrationForm()
                form.username.data = username
                form.password.data = password
                form.email.data = email

                u.add_user(form)

            user = User.query.first()
            assert user.username == username
            assert user.email == email
            assert check_hashed_password(user.password, password)

    def test_is_valid_user(self, test_user_1, test_user_2) -> None:
        with app.test_request_context():
            form = LoginForm()
            form.email.data = 'test@email.com'
            form.password.data = 'testPassword'

        assert u.is_valid_user(test_user_1, form)
        assert not u.is_valid_user(test_user_2, form)
        assert not u.is_valid_user(None, form)

    def test_get_number_of_all_messages(self, test_user_1, test_user_2, test_channel) -> None:
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(test_user_1)
            db.session.add(test_user_2)
            db.session.add(test_channel)
            with app.test_client() as c:
                rv = login(c, test_user_1.email, 'testPassword')
                assert 'Log out' in str(rv.data)
                assert u.get_number_of_all_messages() == 0
                db.session.add(Message(content='_', time=datetime.utcnow(), user_id=1, channel_id=1))
                assert u.get_number_of_all_messages() == 1

                for _ in range(10):
                    db.session.add(Message(content='_', time=datetime.utcnow(), user_id=2, channel_id=1))

                assert u.get_number_of_all_messages() == 1

            with app.test_client() as c:
                rv = login(c, test_user_2.email, 'testPassword')
                assert 'Log out' not in str(rv.data)
                rv = login(c, test_user_2.email, 'testPassword2')
                assert 'Log out' in str(rv.data)
                assert u.get_number_of_all_messages() == 10

    def test_get_number_of_all_channels(self, test_user_1, test_user_2, test_channel) -> None:
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(test_user_1)
            db.session.add(test_user_2)
            db.session.add(test_channel)
            with app.test_client() as c:
                rv = login(c, test_user_1.email, 'testPassword')
                assert 'Log out' in str(rv.data)
                assert u.get_number_of_all_channels() == 0
                db.session.add(ChannelAllowList(user_id=1, channel_id=1))
                assert u.get_number_of_all_channels() == 1

            with app.test_client() as c:
                rv = login(c, test_user_2.email, 'testPassword')
                assert 'Log out' not in str(rv.data)
                rv = login(c, test_user_2.email, 'testPassword2')
                assert 'Log out' in str(rv.data)
                assert u.get_number_of_all_channels() == 0
                db.session.add(ChannelAllowList(user_id=2, channel_id=1))
                assert u.get_number_of_all_channels() == 1

    def test_update_user(self, test_user_1, test_user_2):
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(test_user_1)
            db.session.add(test_user_2)
            with app.test_client() as c:
                rv = login(c, test_user_1.email, 'testPassword')
                assert 'Log out' in str(rv.data)
                assert test_user_1.username == 'testUsername'
                assert test_user_1.email == 'test@email.com'
                assert test_user_2.username == 'testUsername2'
                assert test_user_2.email == 'test2@email.com'

                u.update_user('testUsername3', 'test3@email.com')
                assert test_user_1.username == 'testUsername3'
                assert test_user_1.email == 'test3@email.com'
                assert test_user_2.username == 'testUsername2'
                assert test_user_2.email == 'test2@email.com'

    def test_remove_old_profile_picture(self, test_user_1) -> None:
        app.config['WTF_CSRF_ENABLED'] = False
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(test_user_1)
            with app.test_client() as c:
                _ = login(c, test_user_1.email, 'testPassword')
                file = 'default.png'
                assert os.path.exists(u.get_profile_picture_full_path(file))

                new_file = 'test.png'
                new_absolute_path = u.get_profile_picture_full_path(new_file)
                assert not os.path.exists(new_absolute_path)

                with open(new_absolute_path, 'w') as _:
                    pass

                assert os.path.exists(new_absolute_path)

                User.query.first().profile_picture = new_file
                u.remove_old_profile_picture()
                assert not os.path.exists(new_absolute_path)

    def test_make_square(self) -> None:
        image = Image.new('RGB', (500, 500), (0, 0, 0, 0))
        new_image = u.make_square(image)
        assert new_image.size == (125, 125)
        assert new_image.getpixel((0, 0)) == (0, 0, 0)
        assert new_image.getpixel((36, 89)) == (0, 0, 0)
        assert new_image.getpixel((124, 124)) == (0, 0, 0)

        image = Image.new('RGB', (105, 65), (0, 0, 0, 0))
        new_image = u.make_square(image)
        assert new_image.size == (125, 125)
        assert new_image.getpixel((0, 0)) == (255, 255, 255)

        assert new_image.getpixel((9, 29)) == (255, 255, 255)
        assert new_image.getpixel((10, 30)) == (0, 0, 0)

        assert new_image.getpixel((114, 29)) == (255, 255, 255)
        assert new_image.getpixel((114, 30)) == (0, 0, 0)

        assert new_image.getpixel((94, 29)) == (255, 255, 255)
        assert new_image.getpixel((93, 30)) == (0, 0, 0)
