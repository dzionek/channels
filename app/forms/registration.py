from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError

from app.models.user import User

"""
Module containing the registration form.
"""

class RegistrationForm(FlaskForm):
    """Form shown when user want to register.

    Fields:
        username: Name of the user.\n
        email: Email of the user.\n
        password: Password of the user.\n
        confirm_password: The same password repeated for the second time.\n
        submit: Submit the form.\n

    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username: StringField) -> None:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Choose a different one.')

    def validate_email(self, email: StringField) -> None:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Choose a different one.')
