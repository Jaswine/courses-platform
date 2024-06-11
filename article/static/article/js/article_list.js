document.addEventListener('DOMContentLoaded', () => {
    const showAllCourses = document.querySelector('#ShowAllCourses');
    const searchForm = document.querySelector('#searchForm');
    const filtersButton = document.querySelector('#filtersButton')
    const showFilters = document.querySelector('#ShowFilters');
    const user__status = document.querySelector('.user__status', 'None')


    const getAllArticles = async (
            search= '',
            sort_by = '',
            tags = '',
    ) => {
        /*
        *   Get All articles
        */
        try {
            const response = await fetch(`/api/article/article-list?q=${search}&sort_by=${sort_by}&tags=${tags}`);
            const data = await response.json()

            if (data.status === 'success') {
                renderArticles(data.articles)
            }
        } catch (error) {
            console.error('ERROR: ', error)
        }
    }

    const renderArticles = (articles) => {
        /*
        *   Render Articles
        * */
        showAllCourses.innerHTML = ''

        if (articles.length > 0) {
            articles.forEach((article, index) => {
                renderArticle(article)
            })
        } else {
            // Если статьи не найдены выводить, что они не найдены
            showAllCourses.innerHTML = `
                <div class='courses__not_found'>
                    <h2>Articles not found 🧐</h2>
                </div>
            `
        }
    }

    const renderArticle = (article) => {
        /*
        *   Render Article
        * */
        const div = document.createElement('div')

        // Присвание класса и индификатора
        div.id = article.id
        div.classList.add('course')

        // Добавления внутренностей для курса
        div.innerHTML = `
            <div class='course__header'>
                <a href='/article/${article.id}'>${article.title}</a>
                ${user__status? user__status.value == 'True' ? `
                    <img src='/static/media/icons/MenuVertical.svg' 
                        alt='MenuVertical' 
                        class='course__header__menu' />
                    <div class='course__header__options'>
                        <a href='/article/${article.id}/edit'>Edit</a>
                        <a href='/article/${article.id}/delete'>Delete</a>
                    </div>
                `: '' : ""}
            </div>
            <div class='course__pod__header'>
                <a href='/users/${article.user}'>${article.user}</a>
                <span>${article.created}</span>
            </div>
            <img ${article.image ? `src='${article.image}' ` : 'src="https://images.unsplash.com/photo-1519327128442-131d250b06b8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjR8fG5vdCUyMGZvdW5kfGVufDB8fDB8fHww&auto=format&fit=crop&w=800&q=60"'} alt='${article.title}'/>
            <div class='course__tags></div>
        `

        const courseTagsContainer = document.createElement('div')
        courseTagsContainer.classList.add('course__tags')

        // Взятие всех тегов и добавления их к карточки курса
        article.tags.forEach(tag => {
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
                <div>
                    <i class="fa-solid fa-eye"></i>
                    <span>${article.views_count}</span>
                </div>
                <form>
                    <i class="fa-solid fa-heart heart" style="${article.liked_for_this_user ? 'color: #EAB6E1': 'color: #202020'}"></i>
                    <span>${article.likes_count}</span>
                </form>
                <div>
                    <i class="fa-solid fa-message comment"></i>
                    <span>${article.comments_count}</span>
                </div>
            </div>
            <div class='course__footer__right'>
                
            </div>
        </div>
        `

        showAllCourses.appendChild(div)
    }

    showAllCourses.addEventListener('click', (e) => {
        if (e.target.classList.contains('heart')) {
            //
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

    getAllArticles()
})