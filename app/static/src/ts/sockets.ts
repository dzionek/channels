import io from 'socket.io-client'
import {channelSwitcher, appendMessage} from './messages'

const channelTemplate = require('../../handlebars/channel.handlebars')

const socket: SocketIOClient.Socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

interface ChannelSocketResponse {
    readonly channelName: string
}

interface MessageSocketResponse {
    readonly user: string
    readonly time: string
    readonly channel: string
    readonly messageContent: string
}

export function sockets(): void {
    show_added_channel()
    show_added_message()
}

function show_added_channel(): void {
    socket.on('announce channel', (data: ChannelSocketResponse) => {
        const li = channelTemplate({'channelName': data.channelName})
        const channelsList: HTMLDivElement = document.querySelector('#channels-list ul')
        channelsList.innerHTML += li
        channelSwitcher()
    })
}

function show_added_message(): void {
    socket.on('announce message', (data: MessageSocketResponse) => {
        appendMessage(data.user, data.time, data.messageContent)
    })
}