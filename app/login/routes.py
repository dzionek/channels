from flask import render_template, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user

from typing import Union
from werkzeug.wrappers import Response

from .base import login
from .utils import set_up_app, add_user, is_valid_user

from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm

from app.models.user import User

"""
Routes for the functionality of the app related to login.
"""

@login.route('/', methods=['GET', 'POST'])
def index() -> str:
    """Handle the login process.

    Opened with GET:
        Check if the user is logged in. If it is, redirect to the app.
        Otherwise, render template to log in.

    Opened with POST:
        Get 'username' parameter from the POST form. Log in user of a given 'username'
        and redirect her/him to app if she/he entered valid credentials. Otherwise, show
        message that login was unsuccessful.

    Returns:
        By default, the rendered login page.
        If received valid POST form, the rendered app page.

    """
    if current_user.is_authenticated:
        return set_up_app()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if is_valid_user(user, form):
            login_user(user=user, remember=form.remember)
            return set_up_app()
        else:
            flash('Login Unsuccessful. Incorrect email or password', 'danger')

    return render_template('login.html', form=form)

@login.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    """Handle the registration process.

    Opened with GET:
        Render the registration form.

    Opened with POST:
        Create the user and redirect to the login page. Otherwise, show what was invalid in the form.

    Returns:
        By default, the rendered registration page.
        If received valid POST form, the redirection to the login page.

    """
    form = RegistrationForm()
    if form.validate_on_submit():
        add_user(form)
        flash(f'An account was successfully created for {form.username.data}!', 'success')
        return redirect(url_for('login.index'))
    else:
        return render_template('register.html', form=form)

@login.route('/log-out')
def log_out() -> Response:
    """Log out the current user and redirect to the login page.

    Returns:
        Redirection to the login page.

    """
    logout_user()
    return redirect(url_for('login.index'))