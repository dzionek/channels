/**
 * Module responsible for adding a channel and handling its modal.
 */

/**
 * JSON response after sending add channel request to server.
 */
interface AddChannelResponse {
    readonly success: boolean
    readonly errorMessage?: string
}

/**
 * Get server response from add channel request to server.
 * @param channelName  name of the channel to be added.
 * @return Promise with JSON of the response.
 */
function getResponseAddChannel(channelName: string): Promise<AddChannelResponse> {
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
export function addChannelModal(): void {

    const input: HTMLButtonElement = document.querySelector('#add-channel-input')
    const addButton: HTMLButtonElement = document.querySelector('#add-channel-add-button')

    addButton.addEventListener('click', async () => {
        const channelName: string = input.value
        const responseAddChannel: AddChannelResponse = await getResponseAddChannel(channelName)
        if (responseAddChannel.success) {
            addChannelMessage()
            closeModal()
        } else {
            invalidChannelName(responseAddChannel.errorMessage)
        }
    })
}