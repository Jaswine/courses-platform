import {showHideElement, showHideElementShow, showHideElementHide} from './show_hide_element.js'
import {createGlobalMessage} from "./globalMessage.js";
import {sendData} from './sendData.js'

const COMPLAINT_LIST  = [
    'Unwanted advertising or spam',
    'Pornography or explicit sex scenes',
    'Discriminatory language or naturalistic content',
    'Propaganda of terrorism',
    'Harassment or bullying',
    'Suicide or self-mutilation',
    'False information',
]

export async function complaintGlobalWindow(csrfToken, TaskId) {
 return new Promise((resolve) => {
      const div = document.createElement('form')
      div.method = 'POST'
      div.classList.add('confirm__global__window')

      div.addEventListener('submit', (e) => {
          e.preventDefault()

         let formData = new FormData(div)
         formData.append('message', '')

          showHideElementHide(div_form)
          showHideElementHide(div)

          return resolve(formData)
      })

      const input_csrf_token = document.createElement('input')
      input_csrf_token.type = 'hidden'
      input_csrf_token.name = 'csrfmiddlewaretoken'
      input_csrf_token.value = csrfToken.value
      div.appendChild(input_csrf_token)

      const div_form = document.createElement('div')
      div_form.classList.add('confirm__global__window__form', 'complaint__global__window__form')

      const div_text = document.createElement('h2')
      div_text.innerHTML = 'Cause of complaint'
      div_form.appendChild(div_text)

      const div_complaints_selections = document.createElement('div')
      div_complaints_selections.classList.add('confirm__complaints_selections')

     COMPLAINT_LIST.forEach((complaint, index) => {
         const radio_field = document.createElement('div')
         radio_field.classList.add('confirm__complaints_selections__field')

         const radio_field_label = document.createElement('label')
         radio_field_label.innerHTML = complaint

         const input = document.createElement('input')
         input.type = 'radio'
         input.name = 'type'
         input.required = true
         input.value = complaint

         radio_field.appendChild(input)
         radio_field.appendChild(radio_field_label)
         div_complaints_selections.appendChild(radio_field)
     })

      const div_buttons = document.createElement('div')
      div_buttons.classList.add('confirm__global__window__buttons')

      const confirm_button = document.createElement('button')
      confirm_button.classList.add('btn')
      confirm_button.type = 'submit'
      confirm_button.innerHTML = `<i class="fa-solid fa-check"></i> Confirm`

      const cancel_button = document.createElement('button')
      cancel_button.classList.add('btn', 'btn--primary')
      cancel_button.innerHTML = `<i class="fa-solid fa-ban"></i> Cancel`
      cancel_button.addEventListener('click', () => {
          showHideElementHide(div_form)
          showHideElementHide(div)
          resolve(false)
      })

      div_buttons.appendChild(cancel_button)
      div_buttons.appendChild(confirm_button)

      div_form.appendChild(div_complaints_selections)
      div_form.appendChild(div_buttons)
      div.appendChild(div_form)

      document.body.appendChild(div)
 })
}