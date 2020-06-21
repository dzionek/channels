from app import create_app

"""
Main module of the app which is responsible for running it.
"""

def main() -> None:
    """Run the application."""
    app = create_app()
    app.run()


if __name__ == '__main__':
    main()