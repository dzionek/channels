import io from 'socket.io-client'
import {channelSwitcher, appendMessage} from './messages'

/**
 * Module handling Socket.IO with callback functions when certain socket was triggered.
 */

/** Handlebars template of the channel in channels' list. */
const channelTemplate = require('../../handlebars/channel.handlebars')

/** Address of the socket used in this module. */
const socket: SocketIOClient.Socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

/**
 * JSON response emitted after adding a channel.
 */
interface ChannelSocketResponse {
    readonly channelName: string
}

/**
 * JSON response emitted after sending a message.
 */
interface MessageSocketResponse {
    readonly userName: string
    readonly userPicture: string
    readonly time: string
    readonly messageContent: string
}

/**
 * Main Socket.IO function adding listeners for each events.
 */
export function sockets(): void {
    show_added_channel()
    show_added_message()
}

/**
 * When 'announce channel' is emitted, get its name and add it to HTML.
 */
function show_added_channel(): void {
    socket.on('announce channel', (data: ChannelSocketResponse) => {

        // if there is alert informing "there are no channels", it must be closed.
        const alert: HTMLDivElement = document.querySelector('.alert-danger')
        if (alert != null) {
            alert.remove()
        }

        const li = channelTemplate({'channelName': data.channelName})
        const channelsList: HTMLDivElement = document.querySelector('#channels-list ul')
        channelsList.innerHTML += li
        channelSwitcher()
    })
}

/**
 * When 'announce message' is emitted, get all its data and add it to HTML.
 */
function show_added_message(): void {
    socket.on('announce message', (data: MessageSocketResponse) => {
        appendMessage(data.userName, data.userPicture, data.time, data.messageContent)
    })
}