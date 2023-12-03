document.addEventListener("DOMContentLoaded", () => {
    let form = document.querySelector('#CreateTitleForm')
    const course_id = document.querySelector('#CourseId').value
    const course_data = document.querySelector('#CourseData')
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let messages = document.querySelector('.messages');

    const getData = () => {
        fetch(`/api/courses/${course_id}/titles/`)
            .then(response => response.json())
            .then(data => {
                course_data.innerHTML = ""

                if (data.message == "Titles not found") {
                    course_data.innerHTML = `<h2>${data.message}</h2>`
                } else {
                    console.log(data)

                    data.titles.map(title => {
                        const div = document.createElement('div');
                        div.classList.add('course__title')
                        div.id = title.id

                        const title_form = document.createElement('form');
                        title_form.method = 'POST'
                        title_form.classList.add('course__title__header')

                        title_form.innerHTML = `
                          <input 
                                type="text" 
                                name="title" 
                                value="${title.title}" 
                                class = "course__title__header__change"
                                placeholder="Enter a title for the course..." />
                            <div>
                                <button 
                                    class="${title.public? 'fa-solid fa-eye': 'fa-solid fa-eye-slash' }  course__title__header__public" 
                                    title="${title.public? 'Public': 'Non-public'}"></button>
                                <button 
                                    class="fa-solid fa-trash course__title__header__remove" 
                                    title="Remove"></button>
                                <a 
                                    class="fa-solid fa-circle-plus course__title__header__add__new__task " 
                                    title="Add new task" 
                                    href="/courses/${course_id}/title/${title.id}/tasks-create"></a>
                                <button 
                                    class="fa-solid fa-sort-down course__title__header__open" 
                                    title="Open"></button>
                            </div>
                        `
                        div.appendChild(title_form)

                        const title_tasks = document.createElement('div');
                        title_tasks.classList.add('title__tasks')
                        title_tasks.style.display = "none"
                        title_tasks.style.opacity = 0

                        if (title.tasks.length > 0) {
                            title.tasks.forEach(task => {
                                console.log(task)
                                const task_div = document.createElement('form');
                                task_div.method = 'POST'
                                task_div.classList.add('title__task')
                                task_div.id = `task_${task.id}`

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

                                task_div.innerHTML = `
                                    ${image_type}
                                    <input
                                        type="text"
                                        name="task_title"
                                        value="${task.title}"
                                        placeholder="Enter task title..."
                                        class="course__task__change"/>
                                    <div>
                                        <button
                                            class="${task.public? 'fa-solid fa-eye': 'fa-solid fa-eye-slash' }  course__task__public"
                                            title="${task.public? 'Public': 'Non-public'}"></button>
                                        <a
                                            class="fa-solid fa-pen-clip course__task__update"
                                            title="Update task"
                                            href="/courses/${course_id}/title/${title.id}/tasks-update/${task.id}"></a>
                                        <button
                                            class="fa-solid fa-trash course__task__remove"
                                            title="Remove"></button>
                                    </div>
                                `

                                title_tasks.appendChild(task_div)
                            })
                        }

                        div.appendChild(title_tasks)

                        course_data.appendChild(div)

                    })

                }

                const title__change__tags = document.querySelectorAll('.course__title__header__change')

                title__change__tags.forEach(tag => {
                    tag.addEventListener('change', (e) => {
                        let title = e.target.parentNode.parentNode

                        const formData = new FormData(e.target.parentNode);
                        formData.append('csrfmiddlewaretoken', csrfToken.current);

                        fetch(`/api/courses/titles/${title.id}/`, {
                            method: 'POST',
                            body: formData
                        })
                            .then(response => response.json())
                            .then(data => {
                                getData()
                            })
                            .catch(error => {
                                console.log(error.message)
                            })
                    })
                })

                const course__task__changes = document.querySelectorAll('.course__task__change')

                course__task__changes.forEach(tag => {
                    tag.addEventListener('change', (e) => {
                        let task = e.target.parentNode
                        console.log(task)

                        const formData = new FormData(e.target.parentNode);
                        formData.append('csrfmiddlewaretoken', csrfToken.current);

                        fetch(`/api/courses/${course_id}/tasks/${parseInt(task.id.slice(5))}/`, {
                            method: 'POST',
                            body: formData
                        })
                            .then(response => response.json())
                            .then(data => {
                                getData()
                            })
                            .catch(error => {
                                console.log(error.message)
                            })
                    })
                })
            })
            // .catch(error => {
            //     console.log(error.message)
            // })
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault()

        let data = new FormData(form)
        fetch(`/api/courses/${course_id}/titles/`, {
            method: 'POST',
            body: data
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                getData()
            })
            .catch(error => {
                console.log(error)
                console.log(error.message)
            })
    })

    course_data.addEventListener('click', (e) => {
        e.preventDefault()

        // Change title's type (public or private)
        if (e.target.classList.contains('course__title__header__public')) {
            const title = e.target.parentNode.parentNode.parentNode
            const answer = confirm('Are you sure?')

            if (answer) {
                const formData = new FormData();
                formData.append('public', e.target.title == 'Public' ? true: false);
                formData.append('csrfmiddlewaretoken', csrfToken.current);

                fetch(`/api/courses/titles/${title.id}/`, {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        getData()
                    })
                    .catch(error => {
                        console.log(error.message)
                    })
            }
        }

        // Remove title
        if (e.target.classList.contains('course__title__header__remove')) {
            const title = e.target.parentNode.parentNode.parentNode;

            const answer = confirm('Are you sure you want to delete this item?')

            if (answer) {
                fetch(`/api/courses/titles/${title.id}/`, {
                    method: 'DELETE',
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        getData()
                    })
                    .catch(error => {
                        console.log(error.message)
                        getData()
                    })
            }
        }

        // Open issues under title
        if (e.target.classList.contains('course__title__header__open')) {
            const title = e.target.parentNode.parentNode.parentNode
            const tasks = title.querySelector('.title__tasks')
            if (tasks.style.display == 'none') {
                tasks.style.display = 'flex'

                setTimeout(() => {
                    tasks.style.opacity = 1
                })
            } else {
                setTimeout(() => {
                    tasks.style.opacity = 0
                })

                tasks.style.display = 'none'
            }
        }

          // Open issues under title
          if (e.target.classList.contains('course__title__header__add__new__task')) {
            window.location.href = e.target.href
          }

          if (e.target.classList.contains('course__task__public')) {
            const task = e.target.parentNode.parentNode
            const answer = confirm('Are you sure?')

            if (answer) {
                const formData = new FormData();
                formData.append('public', e.target.title == 'Public' ? true: false);
                formData.append('csrfmiddlewaretoken', csrfToken.current);

                fetch(`/api/courses/${course_id}/tasks/${parseInt(task.id.slice(5))}/`, {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        getData()
                    })
                    .catch(error => {
                        console.log(error.message)
                    })
            }
          }

          if (e.target.classList.contains('course__task__update')) {
            const task = e.target.parentNode.parentNode
            window.location.href = `/courses/${course_id}/edit/tasks/${parseInt(task.id.slice(5))}/edit/`
          }

          if (e.target.classList.contains('course__task__remove')) {
            const task = e.target.parentNode.parentNode
            const answer = confirm('Are you sure you want to delete this item?')

            if (answer) {
                fetch(`/api/courses/${course_id}/tasks/${parseInt(task.id.slice(5))}/`, {
                    method: 'DELETE',
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        getData()
                    })
                    .catch(error => {
                        console.log(error.message)
                        getData()
                    })
            }
          }

    })

    getData()
})