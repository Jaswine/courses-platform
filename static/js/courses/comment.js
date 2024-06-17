document.addEventListener('DOMContentLoaded', () => {
 const CourseId = document.querySelector('#CourseId').value
 const TaskId = document.querySelector('#TaskId').value

 const form = document.querySelector('#CreateTaskCommentForm')
 const list = document.querySelector('#TaskCommentList')
 const messageList = document.querySelector('#MessageList')

const user__status = document.querySelector('.user__status', 'None')

const getTaskComments = async (path) => {
    const response = await fetch(path)
    const data = await response.json()

    if (data.status == 'success') {
        renderTaskComments(data.comments)
    }
}

 const renderTaskComments = (comments) => {
    list.innerHTML = ''
    if (comments.length > 0) {
        comments.forEach((comment, index) => {
            console.log(comment)
            renderTaskComment(comment)
        })
    }
  }

  const renderTaskComment = (comment) => {
     const div = document.createElement('div')
     div.classList.add('comment_item')

      // TODO: Create comment's header
      const div_header = document.createElement('div')
      div_header.classList.add('comment_item__header')

      const div_header_left = document.createElement('div')
      div_header_left.classList.add('comment_item__header__left')
      div_header_left.innerHTML += `<img src="${comment.user.ava}" alt="${comment.user.username}" />`
      div_header_left.innerHTML += `<a href="/users/${comment.user.username}">${comment.user.username}</a>`

      const div_header_right = document.createElement('img')
      div_header_right.src = '/static/media/icons/MenuVertical.svg'
      div_header_right.alt = 'MenuVertical'

      div_header.appendChild(div_header_left)
      div_header.appendChild(div_header_right)
      div.appendChild(div_header)

      // TODO: Create comment's text
      const div_text = document.createElement('div')
      div_text.classList.add('comment_item__text')
      div_text.innerHTML = comment.message
      div.appendChild(div_text)

      // TODO: Create comment's footer
      const div_footer = document.createElement('div')
      div_footer.classList.add('comment_item__footer')

      const div_footer_left = document.createElement('div')
      div_footer_left.classList.add('comment_item__footer__left')

      const div_footer_left_smile_button = document.createElement('a')
      div_footer_left_smile_button.classList.add('material-symbols-outlined')
      div_footer_left_smile_button.innerHTML = `sentiment_satisfied`
      div_footer_left_smile_button.addEventListener('click', () => {

      })

      const div_footer_left_span = document.createElement('u')

      const div_footer_left_reply_button = document.createElement('a')
      div_footer_left_reply_button.innerHTML = `Reply`
      div_footer_left_reply_button.addEventListener('click', () => {

      })

      div_footer_left.appendChild(div_footer_left_smile_button)
      div_footer_left.appendChild(div_footer_left_span)
      div_footer_left.appendChild(div_footer_left_reply_button)

      const div_footer_right = document.createElement('span')
      div_footer_right.innerHTML += comment.created

      div_footer.appendChild(div_footer_left)
      div_footer.appendChild(div_footer_right)
      div.appendChild(div_footer)

      list.appendChild(div)
  }

  form.addEventListener('submit', (e) => {
      e.preventDefault()

      if (form.querySelector('textarea').value.length < 4) {
        createGlobalMessage('Message is too short!')
      } else if (form.querySelector('textarea').value.length > 1000) {
        createGlobalMessage('Message is too long!')
      } else {
        let formData = new FormData(form)

        sendData(`/api/courses/tasks/${TaskId}/comments`, formData)
      }
  })

  const sendData = async (path, data) => {
     await fetch(path, {
            method: 'POST',
            body: data
        })
            .then(response => response.json())
            .then(d => {
                console.log(d)
                createGlobalMessage("Message created successfully!")
                getTaskComments(`/api/courses/tasks/${TaskId}/comments`)
            })
            .catch(error => {
                console.error('ERROR: \n\n', error)
            })
  }

  const createGlobalMessage = (message) => {
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

  getTaskComments(`/api/courses/tasks/${TaskId}/comments`)
})