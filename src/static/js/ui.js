"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
/**
 * Get server response from add channel request to server.
 * @param channelName  name of the channel to be added.
 * @return Promise with JSON of the response.
 */
function getResponseAddChannel(channelName) {
    return new Promise((resolve) => {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/add-channel');
        xhr.responseType = 'json';
        xhr.onload = () => {
            resolve(xhr.response);
        };
        const form = new FormData();
        form.append('channelName', channelName);
        xhr.send(form);
    });
}
/**
 * Close the modal after adding a channel.
 */
function closeModal() {
    const closeButton = document.querySelector('#add-channel-close-button');
    closeButton.click();
}
/**
 * Show an alert after sending an invalid channel name.
 * @param error  error message.
 */
function invalidChannelName(error) {
    alert(`Invalid channel name, error message: ${error}.`);
}
/**
 * Show an alert after successfully adding a channel.
 */
function addChannelMessage() {
    alert('The channel was successfully added!');
}
/**
 * Manage the add channel modal. If input field has a valid channel name, create a channel.
 * Otherwise, show a corresponding error.
 */
function addChannelModal() {
    const input = document.querySelector('#add-channel-input');
    const addButton = document.querySelector('#add-channel-add-button');
    addButton.addEventListener('click', () => __awaiter(this, void 0, void 0, function* () {
        const channelName = input.value;
        const responseAddChannel = yield getResponseAddChannel(channelName);
        if (responseAddChannel.success) {
            addChannelMessage();
            closeModal();
        }
        else {
            invalidChannelName(responseAddChannel.errorMessage);
        }
    }));
}
/**
 * Global variable to monitor the channel the user is currently looking at.
 */
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
 * Change a channel and show its messages.
 * @param channel  channel to be switched on.
 */
function switchChannel(channel) {
    channel.addEventListener('click', function () {
        return __awaiter(this, void 0, void 0, function* () {
            const hideSwitchChannel = document.querySelector('#hide-switch-channel');
            hideSwitchChannel.style.display = 'block';
            currentChannel = this.dataset.channel;
            const channelNameInfo = document.querySelector('#channel-info h3');
            channelNameInfo.innerHTML = currentChannel;
            const responseMessages = yield getResponseMessages(currentChannel);
            const messages = responseMessages.messages;
            const messagesDiv = document.querySelector('#messages-list');
            messagesDiv.innerHTML = '';
            messages.forEach(message => {
                const ul = document.createElement('ul');
                ul.innerHTML = `<b>${message.user}</b> - ${message.time} : ${message.content}`;
                messagesDiv.append(ul);
            });
        });
    });
}
/**
 * Switch a channel and show its messages after clicking on its panel.
 */
function channelSwitcher() {
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
function sendMessage() {
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
document.addEventListener('DOMContentLoaded', () => {
    addChannelModal();
    channelSwitcher();
    sendMessage();
});
