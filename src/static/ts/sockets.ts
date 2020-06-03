import io from 'socket.io-client'
import * as Handlebars from 'handlebars'

const socket: SocketIOClient.Socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

interface channelSocketResponse {
    readonly channelName: string
}

export function show_added_channel(): void {
    const channelTemplate: Handlebars.Template = Handlebars.compile(
        document.querySelector('#handlebars-channel').innerHTML
    )

    socket.on('announce channel', (data: channelSocketResponse) => {
        console.log(data.channelName)
        const li = channelTemplate({'channelName': data.channelName})
        const channelsList: HTMLDivElement = document.querySelector('#channels-list ul')
        channelsList.innerHTML += li
    })
}