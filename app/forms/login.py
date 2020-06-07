from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

"""
Module containing the login form.
"""

class LoginForm(FlaskForm):
    """Form shown when user want to sign in.

    Fields:
        email: Email of the user.\n
        password: Password of the user.\n
        submit: Submit the form.\n

    """
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')