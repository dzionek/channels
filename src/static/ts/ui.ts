/**
 * JSON response after sending add channel request to server.
 */
interface addChannelJSON {
    success: boolean
    errorMessage?: string
}

/**
 * Get server response from add channel request to server.
 * @param channelName  name of the channel to be added.
 * @return Promise with JSON of the response.
 */
function getResponseAddChannel(channelName: string): Promise<addChannelJSON> {
    return new Promise((resolve) => {
        const xhr: XMLHttpRequest = new XMLHttpRequest()
        xhr.open('POST', '/add-channel')

        xhr.responseType = 'json'

        xhr.onload = () => {
            resolve(xhr.response)
        }

        const form: FormData = new FormData()
        form.append('channelName', channelName)

        xhr.send(form)
    })
}

/**
 * Close the modal after adding a channel.
 */
function closeModal(): void {
    const closeButton: HTMLButtonElement = document.querySelector('#add-channel-close-button')
    closeButton.click()
}

/**
 * Show an alert after sending an invalid channel name.
 * @param error  error message.
 */
function invalidChannelName(error: string): void {
    alert(`Invalid channel name, error message: ${error}.`)
}

/**
 * Show an alert after successfully adding a channel.
 */
function addChannelMessage() {
    alert('The channel was successfully added!')
}

/**
 * Manage the add channel modal. If input field has a valid channel name, create a channel.
 * Otherwise, show a corresponding error.
 */
function addChannelModal(): void {

    const input: HTMLButtonElement = document.querySelector('#add-channel-input')
    const addButton: HTMLButtonElement = document.querySelector('#add-channel-add-button')

    addButton.addEventListener('click', async () => {
        const channelName: string = input.value
        const responseAddChannel: addChannelJSON = await getResponseAddChannel(channelName)
        if (responseAddChannel.success) {
            addChannelMessage()
            closeModal()
        } else {
            invalidChannelName(responseAddChannel.errorMessage)
        }
    })
}

/**
 * Global variable to monitor the channel the user is currently looking at.
 */
let currentChannel: string = undefined

/**
 * JSON response of the single message.
 */
interface singleMessageJSON {
    user: string
    content: string
    time: string
}

/**
 * JSON response of the get messages request to server.
 */
interface messagesJSON {
    messages: singleMessageJSON[]
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
 * Change a channel and show its messages.
 * @param channel  channel to be switched on.
 */
function switchChannel(channel: HTMLElement): void {
    channel.addEventListener('click', async function () {
        const hideSwitchChannel: HTMLDivElement = document.querySelector('#hide-switch-channel')
        hideSwitchChannel.style.display = 'block'

        currentChannel = this.dataset.channel
        const channelNameInfo: HTMLElement = document.querySelector('#channel-info h3')
        channelNameInfo.innerHTML = currentChannel

        const responseMessages: messagesJSON = await getResponseMessages(currentChannel)
        const messages: singleMessageJSON[] = responseMessages.messages
        const messagesDiv: HTMLDivElement = document.querySelector('#messages-list')
        messagesDiv.innerHTML = ''
        messages.forEach(message => {
            const ul = document.createElement('ul')
            ul.innerHTML = `<b>${message.user}</b> - ${message.time} : ${message.content}`
            messagesDiv.append(ul)
        })
    })
}

/**
 * Switch a channel and show its messages after clicking on its panel.
 */
function channelSwitcher(): void {
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
function sendMessage(): void {
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

document.addEventListener('DOMContentLoaded', () => {
    addChannelModal()
    channelSwitcher()
    sendMessage()
})