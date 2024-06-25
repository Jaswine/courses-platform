import {showHideElement, showHideElementShow, showHideElementHide} from './show_hide_element.js'

export async function confirmGlobalWindow(message) {
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