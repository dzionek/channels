/**
 * Module responsible for showing messages after clicking on their channel
 * and for sending a message.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/** Global variable to monitor the channel the user is currently looking at. */
let currentChannel = undefined;
/**
 * Get response with the message of the given channel.
 * @param channelName  name of the channel which messages will be displayed.
 * @return Promise with the messages packed in JSON.
 */
function getResponseMessages(channelName) {
    return new Promise(resolve => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/get-messages');
        xhr.responseType = 'json';
        xhr.onload = () => {
            resolve(xhr.response);
        };
        const data = new FormData();
        data.append('channelName', channelName);
        xhr.send(data);
    });
}
/**
 * Show input field where users can type their messages.
 */
function showInputField() {
    const hideSwitchChannel = document.querySelector('#hide-switch-channel');
    hideSwitchChannel.style.display = 'block';
}
/**
 * Show the title of the {@link currentChannel}.
 */
function showChannelTitle() {
    const channelNameInfo = document.querySelector('#channel-info h3');
    channelNameInfo.innerHTML = currentChannel;
}
/**
 * Show the given messages that belong to the {@link currentChannel}.
 * @param responseMessages  messages of the {@link currentChannel}.
 */
function showChannelsMessages(responseMessages) {
    const messages = responseMessages.messages;
    const messagesDiv = document.querySelector('#messages-list');
    messagesDiv.innerHTML = '';
    messages.forEach(message => {
        const ul = document.createElement('ul');
        ul.innerHTML = `<b>${message.user}</b> - ${message.time} : ${message.content}`;
        messagesDiv.append(ul);
    });
}
/**
 * Change a channel and show its messages.
 * @param channel  channel to be switched on.
 */
function switchChannel(channel) {
    channel.addEventListener('click', function () {
        return __awaiter(this, void 0, void 0, function* () {
            showInputField();
            currentChannel = this.dataset.channel;
            showChannelTitle();
            const responseMessages = yield getResponseMessages(currentChannel);
            showChannelsMessages(responseMessages);
        });
    });
}
/**
 * Switch a channel and show its messages after clicking on its panel.
 */
export function channelSwitcher() {
    const channels = document.querySelectorAll('.channel');
    channels.forEach(channel => switchChannel(channel));
}
/**
 * Add the given message to the database.
 * @param messageContent  content of the message to be added.
 */
function addMessageToDB(messageContent) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/add-message');
    const data = new FormData();
    data.append('messageContent', messageContent);
    data.append('channel', currentChannel);
    xhr.send(data);
}
/**
 * Send the message to the {@link currentChannel} after clicking 'send' button on the website.
 */
export function sendMessage() {
    const sendButton = document.querySelector('#messages-input-send-button');
    sendButton.addEventListener('click', () => {
        const textArea = document.querySelector('#messages-input-text-area');
        const messageContent = textArea.value;
        if (messageContent != '') {
            addMessageToDB(messageContent);
            textArea.value = '';
        }
    });
}
