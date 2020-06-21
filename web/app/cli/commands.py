from .bp import cli_bp
from app.models.base import db

"""
Module containing all custom CLI commands.
"""

@cli_bp.cli.command('create-db')
def create_db() -> None:
    """Create all models into databases."""
    print('All the databases were successfully created!')
    db.create_all()

@cli_bp.cli.command('drop-db')
def create_db() -> None:
    """Drop all databases created from models."""
    print('All the databases were successfully dropped!')
    db.drop_all()
