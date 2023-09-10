document.addEventListener('DOMContentLoaded', () => {
    const ShowAllCourses = document.querySelector('#ShowAllCourses')
    const searchForm = document.querySelector('#searchForm')

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
                            </div>
                            <div class='course__pod__header'>
                                <a href='/users/${course.user}'>${course.user}</a>
                                <span>${course.updated}</span>
                            </div>
                            <div class='course__text'>${course.about}...</div>
                            <img src='/static/${course.image}' alt='${course.title} />
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
                                    <span>${course.likes}</span>
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
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault()

        search = searchForm.querySelector('.search').value
        getCourses()
    })
    
    const filtersButton = document.querySelector('#filtersButton')
    const ShowFilters = document.querySelector('#ShowFilters')
    
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

    ShowFilters.querySelector('#orderByDate').addEventListener('change', (e) => {
        filters[0] = e.target.value
        getCourses()
    })

    // ShowFilters.querySelector('#orderByPopular').addEventListener('change', (e) => {
    //     filters[1] = e.target.value
    //     getCourses()
    // })

    ShowFilters.querySelector('#filterByTag').addEventListener('change', (e) => {
        filters[2] = e.target.value
        getCourses()
    })

    ShowAllCourses.addEventListener('click', (e) => {
        if (e.target.classList.contains('heart')) {
            let course = e.target.parentNode.parentNode.parentNode.parentNode;

            fetch(`/api/courses-like/${course.id}`, {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    let heart = e.target
                    let span = heart.parentNode.querySelector('span')

                    if (data.message == 'User like removed successfully') {
                        heart.style.color = '#202020'
                        span.innerHTML = parseInt(span.innerHTML) - 1
                    } else {
                        heart.style.color = '#EAB6E1'
                        span.innerHTML = parseInt(span.innerHTML) + 1
                    }
                })
                .catch(error => {
                    console.log(error)
                })
                
        }
    })

    getTags()
    getCourses()
})