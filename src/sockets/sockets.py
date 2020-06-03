from .base import socket_io

def announce_channel(channel_name):
    response = {'channelName': channel_name}
    socket_io.emit('announce channel', response, broadcast=True)

def announce_message(user, time, channel, message_content):
    response = {
        'user': user,
        'time': time,
        'channel': channel,
        'messageContent': message_content
    }
    socket_io.emit('announce message', response, broadcast=True)