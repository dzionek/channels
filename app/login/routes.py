from flask import render_template, flash, url_for, redirect
from flask_login import login_user, current_user

from .base import login
from .utils import set_up_app

from app.bcrypt.utils import hash_password, check_hashed_password

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
    if current_user.is_authenticated:
        return set_up_app()

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_hashed_password(user.password, form.password.data):
            login_user(user=user, remember=form.remember)
            return set_up_app()
        else:
            flash('Login Unsuccessful. Incorrect email or password', 'danger')

    return render_template('login.html', form=form)

@login.route('/register', methods=['GET', 'POST'])
def register() -> str:
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        db.session.add(User(
            username=form.username.data, email=form.email.data, password=hashed_password
        ))
        db.session.commit()
        flash(f'An account was successfully created for {form.username.data}!', 'success')
        return redirect(url_for('login.index'))
    return render_template('register.html', form=form)
