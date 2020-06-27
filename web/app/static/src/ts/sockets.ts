import io from 'socket.io-client'
import {appendMessageBottom} from './messages'

/**
 * Module handling Socket.IO with callback functions when certain socket was triggered.
 */

/** Address of the socket used in this module. */
const socket: SocketIOClient.Socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port)

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
    show_added_message()
}

/**
 * When "announce message" is emitted, get all its data and add it to HTML.
 */
function show_added_message(): void {
    socket.on('announce message', (data: MessageSocketResponse) => {
        appendMessageBottom(data.userName, data.userPicture, data.time, data.messageContent)
    })
}