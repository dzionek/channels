import {addChannelModal} from './add-channel'
import {channelSwitcher, sendMessage} from './messages'
import {sockets} from './sockets'

/**
 * Main TS module responsible for calling all UI-related functions after loading the app.
 */

document.addEventListener('DOMContentLoaded', () => {
    addChannelModal()
    channelSwitcher()
    sendMessage()
    sockets()
})