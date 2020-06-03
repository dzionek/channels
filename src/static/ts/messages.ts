/**
 * Module responsible for showing messages after clicking on their channel
 * and for sending a message.
 */

/** Global variable to monitor the channel the user is currently looking at. */
let currentChannel: string = undefined

/**
 * JSON response of the single message.
 */
interface singleMessageJSON {
    readonly user: string
    readonly content: string
    readonly time: string
}

/**
 * JSON response of the get messages request to server.
 */
interface messagesJSON {
    readonly messages: singleMessageJSON[]
}

/**
 * Get response with the message of the given channel.
 * @param channelName  name of the channel which messages will be displayed.
 * @return Promise with the messages packed in JSON.
 */
function getResponseMessages(channelName: string): Promise<messagesJSON> {
    return new Promise<messagesJSON>(resolve => {
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
 * Show the given messages that belong to the {@link currentChannel}.
 * @param responseMessages  messages of the {@link currentChannel}.
 */
function showChannelsMessages(responseMessages: messagesJSON): void {
    const messages: singleMessageJSON[] = responseMessages.messages
    const messagesDiv: HTMLDivElement = document.querySelector('#messages-list')
    messagesDiv.innerHTML = ''
    messages.forEach(message => {
        const ul = document.createElement('ul')
        ul.innerHTML = `<b>${message.user}</b> - ${message.time} : ${message.content}`
        messagesDiv.append(ul)
    })
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

        const responseMessages: messagesJSON = await getResponseMessages(currentChannel)
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