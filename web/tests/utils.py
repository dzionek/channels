"""Utility functions used for unit tests."""

from flask.testing import FlaskClient

def login(client: FlaskClient, email: str, password: str):
    """Log in the user inside the test client."""
    return client.post('/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client: FlaskClient):
    """Log out the user inside the test client."""
    return client.get('/logout', follow_redirects=True)
