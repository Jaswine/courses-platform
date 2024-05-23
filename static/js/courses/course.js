document.addEventListener('DOMContentLoaded', () => {
      const UserId = document.querySelector('#UserId')
      const CourseId = document.querySelector('#CourseId').value
      const TasksContent = document.querySelector('#TasksContent')

      const fetchTitleTasks = async () => {
            const response = await fetch(`/api/courses/${CourseId}/titles/`)
            const data = await response.json()
            renderTitleTasks(data.titles)
      }

      const renderTitleTasks = (titles) => {
            console.log(titles)
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

                  title.tasks.forEach((task, index) => {
                        const div_task = document.createElement('div')
                        div_task.classList.add('task')

                        const div_task__right = document.createElement('div')
                        div_task__right.classList.add('task__left')

                        const div_task_type = document.createElement('span')
                        div_task_type.classList.add('task__done')
                        task.completed_status ? 
                              div_task_type.style.backgroundColor = 'rgb(234, 182, 225)' : 
                              div_task_type.style.backgroundColor = 'transparent'
                        div_task__right.appendChild(div_task_type)

                        let image_type = ""
                        switch (task.type) {
                              case "TaskVideo":
                                    image_type = "<i class='fa-solid fa-clapperboard'></i>"
                                    break
                              case "TaskProject":
                                    image_type = "<i class='fa-solid fa-briefcase'></i>"
                                    break
                              case "TaskQuestions":
                                    image_type = "<i class='fa-solid fa-file-circle-question'></i>"
                                    break
                              case "TaskCode":
                                    image_type = "<i class='fa-solid fa-file-code'></i>"
                                    break
                              default:
                                    image_type = "<i class='fa-solid fa-file-lines'></i>"
                        }

                        div_task__right.innerHTML += image_type

                        const div_task_type_a = document.createElement('a')
                        div_task_type_a.innerHTML = task.title
                        div_task__right.appendChild(div_task_type_a)

                        const div_task__left = document.createElement('div')
                        div_task__left.classList.add('task__right')
                        div_task__left.innerHTML = `
                              <a>
                                    <svg width="13.25" height="23.75" viewBox="0 0 13.25 23.75" fill="none" xmlns="http://www.w3.org/2000/svg">
                                          <path d="M1.26761 1.25L11.8734 11.8558" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                          <path d="M1.25 22.4146L11.8558 11.8088" stroke="#202020" stroke-width="2.5" stroke-linecap="round"/>
                                    </svg>
                              </a>
                        
                        `

                        div_task.appendChild(div_task__right)
                        div_task.appendChild(div_task__left)
                        
                        div.appendChild(div_task)
                  })

                  TasksContent.appendChild(div)
            }
      }
 
      fetchTitleTasks()
})