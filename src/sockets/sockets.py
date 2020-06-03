from .base import socket_io

def announce_channel(channel_name):
    response = {'channelName': channel_name}
    socket_io.emit('announce channel', response, broadcast=True)