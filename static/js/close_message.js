const messages = document.querySelectorAll('.message')
const closes = document.querySelectorAll('.close')

const opacityDisplayNone = (message) => {
    message.style.opacity = 0

    setTimeout(() => {
        message.style.display = 'none'
    }, 300)
}

for (let i = 0; i < messages.length; i++) {
    closes[i].addEventListener('click', () => {
        opacityDisplayNone(messages[i])
    })

    setTimeout(() => {
        opacityDisplayNone(messages[i])
    }, 3000 + 2000 * i )
}