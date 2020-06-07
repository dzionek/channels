from flask import request, render_template

from .base import login
from .utils import log_in, is_logged, set_up_app
from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm

"""
Routes for the functionality of the app related to login.
"""

@login.route('/', methods=['POST', 'GET'])
def index() -> str:
    """Login factory.

    Opened with GET:
        Check if the user is logged in. If it is, redirect to the app.
        Otherwise, render template to log in.

    Opened with POST:
        Get 'username' parameter from the POST form. Create or log in user of a given 'username'
         and redirect her/him to app.

    Returns:
        Template of the login page, or app page.

    """
    if request.method == 'POST':
        return log_in(request.form)
    else:
        if is_logged():
            return set_up_app()
        else:
            form = LoginForm()
            return render_template('login.html', form=form)

@login.route('/register')
def register() -> str:
    form = RegistrationForm()
    return render_template('register.html', form=form)