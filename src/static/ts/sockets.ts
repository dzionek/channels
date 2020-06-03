import io from 'socket.io-client'
import {channelSwitcher} from './messages'

const channelTemplate = require('../handlebars/channel.handlebars')

const socket: SocketIOClient.Socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

interface channelSocketResponse {
    readonly channelName: string
}

export function show_added_channel(): void {
    socket.on('announce channel', (data: channelSocketResponse) => {
        console.log(data.channelName)
        const li = channelTemplate({'channelName': data.channelName})
        const channelsList: HTMLDivElement = document.querySelector('#channels-list ul')
        channelsList.innerHTML += li
        channelSwitcher()
    })
}