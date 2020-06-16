import re

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo

from app.models.channel import Channel

"""
Module containing the forms to add and update a channel.
"""

class ChannelForm(FlaskForm):
    """Base channel form class with methods to validate the email."""

    @staticmethod
    def _channel_has_invalid_name(name: str) -> bool:
        """Check if the channel has invalid name. Its name is invalid if either it is empty,
        has trailing or leading spaces, or violates the `valid_pattern` regex.

        Args:
            name: Name of the channel to be checked.

        Returns:
            True if it has invalid name, False otherwise.

        """
        valid_pattern = re.compile(r'[A-Za-z0-9 \-_]+')

        if not name:
            return True
        else:
            return not(bool(re.fullmatch(valid_pattern, name))) \
                   or name.startswith(' ') \
                   or name.endswith(' ')

    @staticmethod
    def _channel_already_exists(name: str) -> bool:
        """Check if the channel already exists in the database.

        Args:
            name: Name of the channel to be checked.

        Returns:
            True if it already exists, false otherwise.

        """
        channel = Channel.query.filter_by(name=name).first()
        return bool(channel)


class AddChannelForm(ChannelForm):
    name = StringField('Name of the new channel', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit_add = SubmitField('Add a channel')

    def validate_name(self, name: StringField) -> None:
        if self._channel_already_exists(name.data):
            raise ValidationError('This channel name is taken. Choose a different one.')
        elif self._channel_has_invalid_name(name.data):
            raise ValidationError('Name of the channel is invalid.')

class JoinChannelForm(ChannelForm):
    name = StringField('Name of the new channel', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_join = SubmitField('Join the channel')

class UpdateChannelForm(ChannelForm):
    name = StringField('New name of the channel', validators=[DataRequired()])
    submit_update = SubmitField('Update the channel')

    def validate_name(self, name: StringField) -> None:
        if self._channel_already_exists(name.data):
            raise ValidationError('This channel name is either taken or the current name. Choose a different one.')
        elif self._channel_has_invalid_name(name.data):
            raise ValidationError('Name of the channel is invalid.')
