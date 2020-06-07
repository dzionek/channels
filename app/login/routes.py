from flask import render_template, flash, url_for, redirect

from .base import login
from .utils import log_in, is_logged, set_up_app
from app.forms.registration import RegistrationForm
from app.forms.login import LoginForm
from app.models.user import User
from app.models.base import db

"""
Routes for the functionality of the app related to login.
"""

@login.route('/', methods=['GET', 'POST'])
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
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.password == form.password.data:
                return log_in(user.username)
            else:
                flash('Login Unsuccessful. Incorrect email or password', 'danger')
        else:
            flash('Login Unsuccessful. Incorrect email or password', 'danger')
    else:
        if is_logged():
            return set_up_app()

    return render_template('login.html', form=form)

@login.route('/register', methods=['GET', 'POST'])
def register() -> str:
    form = RegistrationForm()
    if form.validate_on_submit():
        db.session.add(User(
            username=form.username.data, email=form.email.data, password=form.password.data
        ))
        db.session.commit()
        flash(f'An account was successfully created for {form.username.data}!', 'success')
        return redirect(url_for('login.index'))
    return render_template('register.html', form=form)
