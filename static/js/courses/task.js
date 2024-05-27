document.addEventListener('DOMContentLoaded', () => {
      const taskList = document.querySelector('#taskList')
      const CourseId = document.querySelector('#CourseId').value
      const TaskId = document.querySelector('#TaskId').value
      var PrevTask = 0
      var NextTask = 0

      const getTasks = async () => {
            const response = await fetch(`/api/courses/${CourseId}/titles/`)   
            const data = await response.json()
            renderTitleTasks(data.titles)
      }

      const renderTitleTasks = (titles) => {
            taskList.innerHTML = ''
            titles.forEach(title => {
                  renderTitle(title)
            });
      }

      const renderTitle = (title) => {
            if (title.public) {
                  const div = document.createElement('div')
                  div.classList.add('tasks__title')
                  
                  const div_header = document.createElement('div')
                  div_header.classList.add('tasks__title__header')

                  const div_h3 = document.createElement('h4')
                  div_h3.innerHTML = title.title
                  div.appendChild(div_h3)

                  div_header.appendChild(div_h3)
                  div.appendChild(div_header)

                  // let 

                  title.tasks.forEach((task, index) => {
                        const div_task = document.createElement('div')
                        div_task.classList.add('task')

                        const div_task__right = document.createElement('div')
                        div_task__right.classList.add('task__left')
                        
                        const div_task_type = document.createElement('span')
                        div_task_type.classList.add('task__done')
                        task.completed_status == 'Completed' ? 
                              div_task_type.style.backgroundColor = 'rgb(234, 182, 225)' : 
                              div_task_type.style.backgroundColor = 'transparent'
                        div_task__right.appendChild(div_task_type)

                        const div_task_type_a = document.createElement('a')
                        div_task_type_a.innerHTML = task.title
                        div_task_type_a.href=`/courses/${CourseId}/${task.id}/`
                        div_task__right.appendChild(div_task_type_a)

                        if (task.id == TaskId) {
                              div_task_type_a.style.color = '#202020'
                        }

                        const div_task__left = document.createElement('div')
                        div_task__left.classList.add('task__right')
                        div_task__left.innerHTML = `
                              <a href='/courses/${CourseId}/${task.id}/'>
                                    <svg style = "opacity:${task.id == TaskId ? '1': ''} "
                                          width="13.25" 
                                          height="23.75" 
                                          viewBox="0 0 13.25 23.75" fill="none" xmlns="http://www.w3.org/2000/svg">
                                          <path d="M1.26761 1.25L11.8734 11.8558" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                          <path d="M1.25 22.4146L11.8558 11.8088" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                    </svg>
                              </a>
                        `

                        div_task.appendChild(div_task__right)
                        div_task.appendChild(div_task__left)
                        
                        div.appendChild(div_task)
                  })

                  taskList.appendChild(div)
            }
      }

      getTasks()
      
})