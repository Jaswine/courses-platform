document.addEventListener('DOMContentLoaded', () => {
      const UserId = document.querySelector('#UserId')
      const CourseId = document.querySelector('#CourseId').value
      const TasksContent = document.querySelector('#TasksContent')
      const enrollDropInACourse = document.querySelector('#enrollDropInACourse')
      var courseRegisterStatus = false

      const CourseLessonsCount = document.querySelector('#CourseLessonsCount')
      const CourseVideosCount = document.querySelector('#CourseVideosCount')
      const CourseExerciesesCount = document.querySelector('#CourseExerciesesCount')
      const CourseProjectsCount = document.querySelector('#CourseProjectsCount')


      const fetchCourseInfo = async () => {
            const response = await fetch(`/api/courses/${CourseId}`)
            const data = await response.json()

            if (data.status == 'success') {
                  RenderButtons(data.data.user_registered)
                  RenderCourseInfo(data.data)
            }
      }

      const RenderButtons = (user_registered) => {
            courseRegisterStatus = user_registered
            let courseContinue = document.querySelector('#CourseContinue')

            if (courseRegisterStatus) {
                  enrollDropInACourse.classList.remove('btn')
                  enrollDropInACourse.innerHTML = 'Drop'

                  courseContinue.style.display = 'block'
            } else {
                  enrollDropInACourse.classList.add('btn')
                  enrollDropInACourse.innerHTML = 'Enroll in a course'

                  courseContinue.style.display = 'none'
            }
      }

      const RenderCourseInfo = (data) => {
            console.log('Status: ', data)
            CourseLessonsCount.innerHTML = `${data.lessons_count} Lessons`
            CourseVideosCount.innerHTML = data.videos_count + " Videos"
            CourseExerciesesCount.innerHTML = data.exercises_count + " Exercises"
            CourseProjectsCount.innerHTML = data.projects_count + " Projects"
      }

      const fetchTitleTasks = async () => {
            const response = await fetch(`/api/courses/${CourseId}/titles/`)
            const data = await response.json()
            renderTitleTasks(data.titles)
      }

      const renderTitleTasks = (titles) => {
            TasksContent.innerHTML = '<h2>📑 Course Program</h2>'
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
                        
                        if (task.completed_status) {
                              const div_task_type = document.createElement('span')
                              div_task_type.classList.add('task__done')
                              task.completed_status == 'Completed' ? 
                                    div_task_type.style.backgroundColor = 'rgb(234, 182, 225)' : 
                                    div_task_type.style.backgroundColor = 'transparent'
                              div_task__right.appendChild(div_task_type)
                        }

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
                        task.completed_status ? div_task_type_a.href=`/courses/${CourseId}/${task.id}/` : ''
                        div_task__right.appendChild(div_task_type_a)

                        const div_task__left = document.createElement('div')
                        div_task__left.classList.add('task__right')
                        div_task__left.innerHTML = `
                              <a ${task.completed_status ? `href='/courses/${CourseId}/${task.id}/'` : ''}>
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
      
      fetchCourseInfo()
      fetchTitleTasks()

      enrollDropInACourse.addEventListener('click', () => {
            fetch(`/api/courses-like/${CourseId}/add-to-course`, {
                  method: 'POST',
              })
                  .then(response => response.json())
                  .then(data => {
                        console.log(data)
                        courseRegisterStatus ? RenderButtons(false) : RenderButtons(true)
                        fetchTitleTasks()
                  })
                  .catch(error => {
                        console.log(error.message)
                  })
      })
})