document.addEventListener('DOMContentLoaded', () => {
 const CourseId = document.querySelector('#CourseId').value
 const TaskId = document.querySelector('#TaskId').value
 const Comments = document.querySelector('#Comments')

 const comments_form = document.querySelector('#CreateTaskCommentForm')
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
      div_header_right.classList.add('comment_item__header__icon')
      div_header_right.src = '/static/media/icons/MenuVertical.svg'
      div_header_right.alt = 'MenuVertical'

      const div_header_right_menu = document.createElement('div')
      div_header_right_menu.classList.add('comment_item__header__menu')

      div_header_right_menu.style.opacity = 0
      div_header_right_menu.style.display = 'none'

      const update_comment_button = document.createElement('div')
      update_comment_button.innerHTML = `<i class="fa-regular fa-pen-to-square"></i> Update`
      div_header_right_menu.appendChild(update_comment_button)

      const delete_comment_button = document.createElement('div')
      delete_comment_button.innerHTML = `<i class="fa-regular fa-trash-can"></i> Delete`
      div_header_right_menu.appendChild(delete_comment_button)

      showHideElement(div_header_right, div_header_right_menu)

      div_header.appendChild(div_header_left)
      div_header.appendChild(div_header_right)
      div_header.appendChild(div_header_right_menu)
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
      div_footer_left_smile_button.classList.add('material-symbols-outlined', 'comment_item__footer__left__smile__button')
      div_footer_left_smile_button.innerHTML = `sentiment_satisfied`

      const div_footer_left_smile_menu = document.createElement('div')
      div_footer_left_smile_menu.classList.add('comment_item__footer__left__smile__menu')

      div_footer_left_smile_menu.style.opacity = 0
      div_footer_left_smile_menu.style.display = 'none'

      const button_smiles = ['👍', '👎', '❤️', '🦄', '👏', '🔥']
      button_smiles.forEach((smile, index) => {
            const div_footer_left_smile_button = document.createElement('button')
            div_footer_left_smile_button.classList.add('comment_item__footer__left__smile__button__icon')
            div_footer_left_smile_button.id = `smileButton${index}`
            div_footer_left_smile_button.innerHTML = smile
            div_footer_left_smile_menu.appendChild(div_footer_left_smile_button)
      })

      showHideElement(div_footer_left_smile_button, div_footer_left_smile_menu)

      const div_footer_left_span = document.createElement('u')

      const div_footer_left_reply_button = document.createElement('a')
      div_footer_left_reply_button.innerHTML = `Reply`

      const div_form = document.createElement('div')
      div_form.classList.add('comment_item__form')

      const div_form_element = createTaskCommentForm(div_form)
      div_form_element.style.opacity = 0
      div_form_element.style.display = 'none'

      showHideElement(div_footer_left_reply_button, div_form_element)

      const div_footer_left_reply__form = document.createElement('form')
      div_footer_left_reply__form.classList.add('comment_item__footer__left__reply__form')

      div_footer_left.appendChild(div_footer_left_smile_button)
      div_footer_left.appendChild(div_footer_left_smile_menu)
      div_footer_left.appendChild(div_footer_left_span)
      div_footer_left.appendChild(div_footer_left_reply_button)

      const div_footer_right = document.createElement('span')
      div_footer_right.innerHTML += comment.created

      div_footer.appendChild(div_footer_left)
      div_footer.appendChild(div_footer_right)
      div.appendChild(div_footer)
      div.appendChild(div_form)

      list.appendChild(div)
  }


  const createTaskCommentForm = (place) => {
      const form = document.createElement('form')
      form.classList.add('comment__form')
      form.method = 'POST'
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

      const textarea = document.createElement('textarea')
      textarea.name = 'message'
      textarea.placeholder = 'Enter your message'

      const form_div = document.createElement('div')
      form_div.classList.add('comment__form__footer')
      form_div.innerHTML += `
        <div></div>
        <button class="btn">Send <i class="fa-regular fa-paper-plane"></i></button>
      `

      form.appendChild(textarea)
      form.appendChild(form_div)

      place.appendChild(form)

      return form
  }

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

  const showHideElement = (button, element) => {
      button.addEventListener('click', () => {
          if (element.style.display === 'flex') {
              element.style.display = 'none'
              element.style.opacity = 0
          } else {
              element.style.opacity = 1
              element.style.display = 'flex'
          }
      })
  }

  createTaskCommentForm(comments_form)

  getTaskComments(`/api/courses/tasks/${TaskId}/comments`)

})