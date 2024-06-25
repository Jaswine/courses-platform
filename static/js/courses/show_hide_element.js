
export function showHideElement (button, element) {
  button.addEventListener('click', () => {
      if (element.style.display === 'flex') {
          showHideElementHide(element)
      } else {
          showHideElementShow(element)
      }
  })
}

export function showHideElementShow (element) {
    element.style.display = 'flex'

  setTimeout(() => {
    element.style.opacity = 1
  }, 300)
}

export function showHideElementHide (element) {
  element.style.opacity = 0

  setTimeout(() => {
    element.style.display = 'none'
  }, 300)
}