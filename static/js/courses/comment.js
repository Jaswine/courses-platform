import { createGlobalMessage } from './globalMessage.js'

const CourseId = document.querySelector('#CourseId').value
const TaskId = document.querySelector('#TaskId').value
const Comments = document.querySelector('#Comments')

const comments_form = document.querySelector('#CreateTaskCommentForm')
const TaskCommentList = document.querySelector('#TaskCommentList')
const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]')
const commentList = document.querySelector('#TaskCommentList')
var url = ''

export function renderTaskComments(list, comments, url) {
    list.innerHTML = '';
    url = url

    comments.forEach(comment => {
        const taskCommentElement = renderTaskComment(comment);
        list.appendChild(taskCommentElement); // Append each top-level comment to the list
    });
}

 const getTaskComments = async (url) => {
    const response = await fetch(url)
    const data = await response.json()

    renderTaskComments(commentList, data.data.comments)
 }

// Recursive function to render a single comment and its children
const renderTaskComment = (comment) => {
    const div = document.createElement('div');
    div.classList.add('comment_item');
    div.id = `comment-${comment.id}`;

    // Create comment's header
    const div_header = document.createElement('div');
    div_header.classList.add('comment_item__header');

    const div_header_left = document.createElement('div');
    div_header_left.classList.add('comment_item__header__left');
    div_header_left.innerHTML += `<img src="${comment.user.ava}" alt="${comment.user.username}" />`;
    div_header_left.innerHTML += `<a href="/users/${comment.user.username}">${comment.user.username}</a>`;

    const div_header_right = document.createElement('img');
    div_header_right.classList.add('comment_item__header__icon');
    div_header_right.src = '/static/icons/MenuVertical.svg';
    div_header_right.alt = 'MenuVertical';

    const div_header_right_menu = document.createElement('div');
    div_header_right_menu.classList.add('comment_item__header__menu');
    div_header_right_menu.style.opacity = 0;
    div_header_right_menu.style.display = 'none';

    const update_comment_button = document.createElement('div');
    update_comment_button.innerHTML = `<i class="fa-regular fa-pen-to-square"></i> Update`;
    div_header_right_menu.appendChild(update_comment_button);

    const delete_comment_button = document.createElement('div');
    delete_comment_button.innerHTML = `<i class="fa-regular fa-trash-can"></i> Delete`;
    div_header_right_menu.appendChild(delete_comment_button);

    delete_comment_button.addEventListener('click', async () => {
        await confirmGlobalWindow("Do you want to delete this comment?").then(async (confirmed) => {
            console.log("User's choice: ", confirmed);
            if (confirmed) {
                await fetch(`/api/courses/tasks/${TaskId}/comments/${comment.id}/delete`, {
                    method: 'DELETE',
                }).then(() => {
                    createGlobalMessage("Message deleted successfully!");
                    div.remove();
                });
            }
        });
    });

    showHideElement(div_header_right, div_header_right_menu);

    div_header.appendChild(div_header_left);
    div_header.appendChild(div_header_right);
    div_header.appendChild(div_header_right_menu);
    div.appendChild(div_header);

    // Create comment's text
    const div_text = document.createElement('div');
    div_text.classList.add('comment_item__text');
    div_text.innerHTML = comment.message;
    div.appendChild(div_text);

    // Create comment's footer
    const div_footer = document.createElement('div');
    div_footer.classList.add('comment_item__footer');

    const div_footer_left = document.createElement('div');
    div_footer_left.classList.add('comment_item__footer__left');

    const div_footer_left_smile_button = document.createElement('a');
    div_footer_left_smile_button.classList.add('comment_item__footer__left__smile__button');
    div_footer_left_smile_button.innerHTML = `<span class="material-symbols-outlined">favorite</span><i>${comment.likes.count}</i>`;
    changeLikeStyle(div_footer_left_smile_button, comment.is_liked);
    div_footer_left_smile_button.addEventListener('click', (e) => {
        fetch(`/api/courses/tasks/${TaskId}/comments/${comment.id}/react/`, {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                let like_count_place =  e.target.parentNode.querySelector('i')
                let like_count = 0

                if (like_count_place) {
                    like_count = like_count_place ? parseInt(like_count_place.innerHTML) : null
                }

                if (data.message === 'Like added successfully!') {
                    if (like_count_place) {
                        like_count_place.innerHTML = like_count+1
                    }

                    changeLikeStyle(div_footer_left_smile_button, true);
                } else {
                     if (like_count_place) {
                        like_count_place.innerHTML = like_count-1
                    }

                    changeLikeStyle(div_footer_left_smile_button, false);
                }
            });
    });

    const div_footer_left_span = document.createElement('u');

    const div_footer_left_reply_button = document.createElement('a');
    div_footer_left_reply_button.innerHTML = `Reply`;

    const div_form = document.createElement('div');
    div_form.classList.add('comment_item__form');

    const div_form_element = createTaskCommentForm(div_form);
    div_form_element.style.opacity = 0;
    div_form_element.style.display = 'none';

    showHideElement(div_footer_left_reply_button, div_form_element);

    div_footer_left.appendChild(div_footer_left_smile_button);
    div_footer_left.appendChild(div_footer_left_span);
    div_footer_left.appendChild(div_footer_left_reply_button);

    const div_footer_right = document.createElement('span');
    div_footer_right.innerHTML = comment.created;

    div_footer.appendChild(div_footer_left);
    div_footer.appendChild(div_footer_right);
    div.appendChild(div_footer);

    // Recursive rendering of child comments
    const div_comments = document.createElement('div');
    div_comments.classList.add('comment_item__comments');

    if (comment.children && comment.children.length > 0) {
        comment.children.forEach(childComment => {
            const childCommentElement = renderTaskComment(childComment);
            div_comments.appendChild(childCommentElement);
        });
    }

    div.appendChild(div_form);
    div.appendChild(div_comments);

    return div;
};


const createTaskCommentForm = (place) => {
  const form = document.createElement('form')
  form.classList.add('comment__form')
  form.method = 'POST'

  const input_csrf_token = document.createElement('input')
  input_csrf_token.type = 'hidden'
  input_csrf_token.name = 'csrfmiddlewaretoken'
  input_csrf_token.value = csrfToken.value

  const textarea = document.createElement('textarea')
  textarea.name = 'message'
  textarea.placeholder = 'Enter your message'

  form.addEventListener('submit', (e) => {
      e.preventDefault()

      if (form.querySelector('textarea').value.length < 4) {
        createGlobalMessage('Message is too short!')
      } else if (form.querySelector('textarea').value.length > 1000) {
        createGlobalMessage('Message is too long!')
      } else {
        let formData = new FormData(form)

        console.log('FORM DATA: ', formData)
        let commentItem = e.target.parentNode.parentNode

        if (commentItem.id) {
            let commentItem_list = commentItem.id.split('-')
            if (commentItem_list[0] == 'comment') {
                formData.append('parent_id', parseInt(commentItem_list[1]))
            }
        }

        sendData(`/api/courses/tasks/${TaskId}/comments`, formData)
        textarea.value = ''
      }
  })

  const form_div = document.createElement('div')
  form_div.classList.add('comment__form__footer')
  form_div.innerHTML += `
    <div></div>
    <button class="btn">Send <i class="fa-regular fa-paper-plane"></i></button>
  `

  form.appendChild(input_csrf_token)
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
            // renderTaskComment(d.comment,TaskCommentList)
            getTaskComments(url)
        })
        .catch(error => {
            console.error('ERROR: \n\n', error)
        })
}

const changeLikeStyle = (button, status) => {
    if (status) {
        button.style.color = '#EAB6E1'
    } else {
        button.style.color = '#bcbcbc'
    }
}

const showHideElement = (button, element) => {
  button.addEventListener('click', () => {
      if (element.style.display === 'flex') {
          showHideElementHide(element)
      } else {
          showHideElementShow(element)
      }
  })
}

const showHideElementShow = (element) => {
    element.style.display = 'flex'

  setTimeout(() => {
    element.style.opacity = 1
  }, 300)
}

const showHideElementHide = (element) => {
  element.style.opacity = 0

  setTimeout(() => {
    element.style.display = 'none'
  }, 300)
}

const confirmGlobalWindow = async (message) => {
 return new Promise((resolve) => {
      const div = document.createElement('div')
      div.classList.add('confirm__global__window')

      const div_form = document.createElement('div')
      div_form.classList.add('confirm__global__window__form')

      const div_text = document.createElement('h2')
      div_text.innerHTML = message
      div_form.appendChild(div_text)

      const div_buttons = document.createElement('div')
      div_buttons.classList.add('confirm__global__window__buttons')

      const yes_button = document.createElement('button')
      yes_button.classList.add('btn')
      yes_button.innerHTML = `<i class="fa-solid fa-check"></i> Yes`
      yes_button.addEventListener('click', () => {
          showHideElementHide(div_form)
          showHideElementHide(div)
          resolve(true)
      })

      const no_button = document.createElement('button')
      no_button.classList.add('btn', 'btn--primary')
      no_button.innerHTML = `<i class="fa-solid fa-ban"></i> Cancel`
      no_button.addEventListener('click', () => {
          showHideElementHide(div_form)
          showHideElementHide(div)
          resolve(false)
      })

      div_buttons.appendChild(no_button)
      div_buttons.appendChild(yes_button)
      div_form.appendChild(div_buttons)
      div.appendChild(div_form)

      document.body.appendChild(div)
 })
}

createTaskCommentForm(comments_form)