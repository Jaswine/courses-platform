document.addEventListener('DOMContentLoaded', () => {
      const task = document.querySelector('.task')
      const taskList = document.querySelector('#TaskList')
      const ShareLesson = document.querySelector('#ShareLesson')
      const FullScreen = document.querySelector('#FullScreen')

      FullScreen.addEventListener('click', () => {
            if (document.fullscreenElement) {
                  FullScreen.style.rotate = '0' 
                  document.exitFullscreen()
            } else {
                  FullScreen.style.rotate = '180deg' 
                  document.documentElement.requestFullscreen()
            }
      })

      
})