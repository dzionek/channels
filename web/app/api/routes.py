"""
All routes of the "API" blueprint.
"""

from flask import render_template
from flask_login import login_required

from .base import api

@api.route('/api-settings')
@login_required
def settings() -> str:
    """Generate API settings page for the user with

    Returns:
        The API settings page with the generated token.

    """
    return render_template('settings-api.html')
