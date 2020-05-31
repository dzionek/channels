import { addChannelModal } from './add-channel.js';
import { channelSwitcher, sendMessage } from './messages.js';
/**
 * Main TS module responsible for calling all UI-related functions after loading the app.
 */
document.addEventListener('DOMContentLoaded', () => {
    addChannelModal();
    channelSwitcher();
    sendMessage();
});
