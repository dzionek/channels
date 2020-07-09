"""
Main module to run the Flask application with web sockets.
"""

from app import socket_io, app

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', debug=True)
