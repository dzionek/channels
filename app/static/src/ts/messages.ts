/**
 * Module responsible for showing messages after clicking on their channel
 * and for sending a message.
 */

/** Handlebars HTML template of the message. */
const messageTemplate = require('../../handlebars/message.handlebars')

/** Global variable to monitor the channel the user is currently looking at. */
let currentChannel: string = undefined

/**
 * JSON response of the single message.
 */
interface SingleMessage {
    readonly userName: string
    readonly userPicture: string
    readonly content: string
    readonly time: string
}

/**
 * JSON response of the get messages request to server.
 */
interface Messages {
    readonly messages: SingleMessage[]
}

/**
 * Get response with the message of the given channel.
 * @param channelName  name of the channel which messages will be displayed.
 * @return Promise with the messages packed in JSON.
 */
function getResponseMessages(channelName: string): Promise<Messages> {
    return new Promise<Messages>(resolve => {
        const xhr: XMLHttpRequest = new XMLHttpRequest()
        xhr.open('POST', '/get-messages')
        xhr.responseType = 'json'
        xhr.onload = () => {
            resolve(xhr.response)
        }
        const data: FormData = new FormData()
        data.append('channelName', channelName)
        xhr.send(data)
    })
}

/**
 * Show input field where users can type their messages.
 */
function showInputField(): void {
    const hideSwitchChannel: HTMLDivElement = document.querySelector('#hide-switch-channel')
    hideSwitchChannel.style.display = 'block'
}

/**
 * Show the title of the {@link currentChannel}.
 */
function showChannelTitle(): void {
    const channelNameInfo: HTMLElement = document.querySelector('#channel-info h3')
    channelNameInfo.innerHTML = currentChannel
}

/**
 * Scroll down to the last message.
 * @param messagesDiv  div where all messages are located.
 */
function scroll_to_last_message(messagesDiv: HTMLDivElement): void {
    messagesDiv.scrollTop = messagesDiv.scrollHeight
}

/**
 * Append a given message to the div of all messages.
 * @param userName  name of the user who sent that message.
 * @param userPicture  profile picture of the user.
 * @param time  time when the message was sent.
 * @param content  content of the message.
 */
export function appendMessage(userName: string, userPicture: string, time: string, content: string): void {
    const messagesList: HTMLUListElement = document.querySelector('#messages-list ul')
    messagesList.innerHTML += messageTemplate({
        'userName': userName,
        'userPicture': userPicture,
        'time': time,
        'content': content
    })
    const messagesDiv = messagesList.parentElement as HTMLDivElement
    scroll_to_last_message(messagesDiv)
}

/**
 * Show the given messages that belong to the {@link currentChannel}.
 * @param responseMessages  messages of the {@link currentChannel}.
 */
function showChannelsMessages(responseMessages: Messages): void {
    const messages: SingleMessage[] = responseMessages.messages
    const messagesList: HTMLDivElement = document.querySelector('#messages-list ul')
    messagesList.innerHTML = ''
    messages.forEach(message => appendMessage(message.userName, message.userPicture, message.time, message.content))
}

/**
 * Change a channel and show its messages.
 * @param channel  channel to be switched on.
 */
function switchChannel(channel: HTMLElement): void {
    channel.addEventListener('click', async function () {
        showInputField()
        currentChannel = this.dataset.channel
        showChannelTitle()

        const responseMessages: Messages = await getResponseMessages(currentChannel)
        showChannelsMessages(responseMessages)
    })
}

/**
 * Switch a channel and show its messages after clicking on its panel.
 */
export function channelSwitcher(): void {
    const channels: NodeListOf<HTMLDivElement> = document.querySelectorAll('.channel')
    channels.forEach(
        channel => switchChannel(channel)
    )
}

/**
 * Add the given message to the database.
 * @param messageContent  content of the message to be added.
 */
function addMessageToDB(messageContent: string): void {
    const xhr: XMLHttpRequest = new XMLHttpRequest()
    xhr.open('POST', '/add-message')
    const data: FormData = new FormData()
    data.append('messageContent', messageContent)
    data.append('channel', currentChannel)
    xhr.send(data)
}

/**
 * Send the message to the {@link currentChannel} after clicking 'send' button on the website.
 */
export function sendMessage(): void {
    const sendButton: HTMLButtonElement = document.querySelector('#messages-input-send-button')
    sendButton.addEventListener('click', () => {
        const textArea: HTMLTextAreaElement = document.querySelector('#messages-input-text-area')
        const messageContent: string = textArea.value
        if (messageContent != '') {
            addMessageToDB(messageContent)
            textArea.value = ''
        }
    })
}