const messageList = document.querySelector('#MessageList')

export function createGlobalMessage (message) {
  const div = document.createElement('div')
  div.classList.add('message')
  div.innerHTML += message

  const close_button = document.createElement('span')
  close_button.classList.add('material-symbols-outlined', 'close')
  close_button.innerHTML = 'close'

  close_button.addEventListener('click', () => {
      div.style.opacity = 0
      messageList.removeChild(div)
  })

  setTimeout(() => {
      div.style.opacity = 0
      messageList.removeChild(div)
  }, 3000)

  div.appendChild(close_button)

  messageList.appendChild(div)
}
