document.addEventListener('DOMContentLoaded', () => {
    const ShowAllCourses = document.querySelector('#ShowAllCourses')
    const searchForm = document.querySelector('#searchForm', '')
    const user__status = document.querySelector('.user__status', 'None')
    console.log(user__status.value)

    // Взятие тэгов для фильтрации
    let search = ''
    let filters = ['', '', '']

    // Функция для взятие всех курсов с фильтрами и поиском
    const getCourses = () => {   
        fetch(`/api/courses?q=${search}&order_by_data=${filters[0]}&order_by_popular=${filters[1]}&filter_by_tag=${filters[2]}`)
            .then((response) => response.json())
            .then(data => {
                ShowAllCourses.innerHTML = ''
                
                // Проверка колличества курсов
                if (data.courses.length > 0) {

                    // Запуск цикла для обработки каждого курса
                    data.courses.forEach(course => {
                        const div = document.createElement('div')
                        
                        // Присвание класса и индификатора
                        div.id = course.id
                        div.classList.add('course')
                        
                        // Добавления внутренностей для курса
                        div.innerHTML = `
                            <div class='course__header'>
                                <a href='/courses/${course.id}'>${course.title}</a>
                                ${user__status? user__status.value == 'True' ? `
                                    <img src='/static/media/icons/MenuVertical.svg' 
                                        alt='MenuVertical' 
                                        class='course__header__menu' />
                                    <div class='course__header__options'>
                                        <a href='/courses/${course.id}/edit'>Edit</a>
                                        <a href='/courses/${course.id}/delete'>Delete</a>
                                    </div>
                                `: '' : ""}
                            </div>
                            <div class='course__pod__header'>
                                <a href='/users/${course.user}'>${course.user}</a>
                                <span>${course.updated}</span>
                            </div>
                            <img ${course.image ? `src='${course.image}' ` : 'src="https://images.unsplash.com/photo-1519327128442-131d250b06b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fG5vdCUyMGZvdW5kfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"'} alt='${course.title}'/>
                            <div class='course__tags></div>
                        `

                        const courseTagsContainer = document.createElement('div')
                        courseTagsContainer.classList.add('course__tags')

                        // Взятие всех тегов и добавления их к карточки курса
                        course.tags.forEach(tag => {
                            const span = document.createElement('a')
                            
                            span.id = `tag${tag.id}`
                            span.classList.add('course__tag')

                            if (tag.id % 3 == 0) {
                                span.style.backgroundColor = 'rgb(208,162,200,60%)'
                            } else if (tag.id % 2 == 0) {
                                span.style.backgroundColor = 'rgb(242,230,217,60%)'
                            } else {
                                span.style.backgroundColor = 'rgb(187,168,253,60%)'
                            }
 
                            span.innerHTML = tag.name 
                            
                            courseTagsContainer.appendChild(span)
                        }) 

                        div.appendChild(courseTagsContainer)

                        // добавления подвала, а точнее дополнительной статистики в виде лайков
                        div.innerHTML += `
                        <div class='course__footer'>
                            <div class='course__footer__left'>
                                <form>
                                    <i class="fa-solid fa-heart heart" style="${course.liked_for_this_user ? 'color: #EAB6E1': 'color: #202020'}"></i>
                                    <span>${course.likes}</span>
                                </form>
                                <div>
                                    <i class="fa-solid fa-message comment"></i>
                                    <span>${course.comments_count}</span>
                                </div>
                            </div>
                            <div class='course__footer__right'>
                                
                            </div>
                        </div>
                        `

                        ShowAllCourses.appendChild(div)
                    });
                } else {
                    // Если курсы не найдены выводить, что они не найдены
                    ShowAllCourses.innerHTML = `
                        <div class='courses__not_found'>
                            <h2>Courses not found 🧐</h2>
                        </div>
                    `
                }
            })
            .catch((error) => {
                // Обработка
                console.error(error)
            })
    }

    // Взятие всех тегов для фильтрации
    const getTags = () => {
        fetch(`/api/tags`)
            .then(response => response.json())
            .then(data => {
                data.tags.forEach(tag => {
                    const option = document.createElement('option')

                    option.value = tag.name
                    option.innerHTML = tag.name

                    filterByTag.appendChild(option)
                })
            })
    }

    // Поиск 
    if (searchForm) {
        searchForm.addEventListener('submit', (e) => {
            e.preventDefault()
    
            search = searchForm.querySelector('.search').value
            getCourses()
        })
    }
    
    const filtersButton = document.querySelector('#filtersButton', '')
    const ShowFilters = document.querySelector('#ShowFilters', '')
    
    if (filtersButton) {
        filtersButton.addEventListener('click', (e) => {
            if (ShowFilters.style.opacity == 0) {
    
                ShowFilters.style.display = 'flex'
                
                setTimeout(() => {
                    ShowFilters.style.opacity = 1
                    ShowFilters.classList.add('animationFormClass')
                }, 200)
    
            } else {
    
                ShowFilters.style.opacity = 0
                ShowFilters.classList.remove('animationFormClass')
    
                setTimeout(() => {
                    ShowFilters.style.display = 'none'
                }, 200)
    
            }
        })
    }

    if (ShowFilters) {
        try {
            ShowFilters.querySelector('#orderByDate').addEventListener('change', (e) => {
                filters[0] = e.target.value
                getCourses()
            })
        
            ShowFilters.querySelector('#filterByTag').addEventListener('change', (e) => {
                filters[2] = e.target.value
                getCourses()
            })
        } catch (error) {
            console.log('Filters not found', error)
        }
    }

    ShowAllCourses.addEventListener('click', (e) => {
        if (e.target.classList.contains('heart')) {
            let course = e.target.parentNode.parentNode.parentNode.parentNode;

            fetch(`/api/courses-like/${course.id}`, {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status == 'success') {
                        let heart = e.target
                        let span = heart.parentNode.querySelector('span')

                        if (data.message == 'User like removed successfully') {
                            heart.style.color = '#202020'
                            span.innerHTML = parseInt(span.innerHTML) - 1
                        } else {
                            heart.style.color = '#EAB6E1'
                            span.innerHTML = parseInt(span.innerHTML) + 1
                        }
                    } else {
                        const div = document.createElement('div')
                        div.classList.add('message')
                        div.innerHTML = `${data.status} - ${data.message}  
                                            <span class="material-symbols-outlined close">
                                                close
                                            </span>`
                        document.querySelector('.messages').appendChild(div)
                    }
                })
                .catch(error => {
                   console.log(error)
                })
                
        }
        
        if (e.target.classList.contains('course__header__menu')) {
            let course = e.target.parentNode.parentNode
            let menu = course.querySelector('.course__header__options')
            
            if (menu.style.opacity == 1) {
                menu.style.opacity = 0
                menu.style.display = 'none'
            } else {
                menu.style.opacity = 1
                menu.style.display = 'flex'
            }
        }
    })

    getTags()
    getCourses()
})