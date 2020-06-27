"""
Main module giving access to command line of the app.
"""

from flask.cli import FlaskGroup
from app import create_app

def main() -> None:
    """Create the application and its command line interface. Give access to this CLI."""
    app = create_app()
    cli = FlaskGroup(app)
    cli()


if __name__ == "__main__":
    main()
