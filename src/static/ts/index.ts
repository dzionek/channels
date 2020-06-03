import {addChannelModal} from './add-channel'
import {channelSwitcher, sendMessage} from './messages'
import {show_added_channel} from './sockets'

/**
 * Main TS module responsible for calling all UI-related functions after loading the app.
 */

document.addEventListener('DOMContentLoaded', () => {
    addChannelModal()
    channelSwitcher()
    sendMessage()
    show_added_channel()
})