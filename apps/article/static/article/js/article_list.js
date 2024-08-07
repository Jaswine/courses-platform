import {showHideElement, showHideElementShow} from '/static/js/courses/show_hide_element.js'

document.addEventListener('DOMContentLoaded', () => {
    const showAllCourses = document.querySelector('#ShowAllCourses');
    const searchForm = document.querySelector('#searchForm');
    const filtersButton = document.querySelector('#filtersButton')
    const showFilters = document.querySelector('#ShowFilters');
    const user__status = document.querySelector('.user__status', 'None')
    const csrfTokenElement = document.querySelector('[name="csrfmiddlewaretoken"]');


    const getAllArticles = async (
            search= '',
            sort_by = '',
            tags = '',
    ) => {
        /*
        *   Взятие всех статей
        */
        try {
            let url = `/api/article/article-list?q=${search}&sort_by=${sort_by}&tags=${tags}`
            const response = await fetch(url);
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

        if (articles.length > 0) {
            const fragment = document.createDocumentFragment();

            articles.forEach(article => {
                fragment.appendChild(renderArticle(article));
            });

            // Очищаем содержимое контейнера и добавляем новые статьи
            showAllCourses.innerHTML = '';
            showAllCourses.appendChild(fragment);
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
                <a href='/articles/${article.id}'>${article.title}</a>
                ${user__status? user__status.value == 'True' ? `
                    <img src='/static/icons/MenuVertical.svg' 
                        alt='MenuVertical' 
                        class='course__header__menu' />
                    <div class='course__header__options'>
                        <a href='/articles/${article.id}/edit'>Edit</a>
                        <a href='/articles/${article.id}/delete'>Delete</a>
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
        article.tags.forEach((tag, index) => {
            const span = document.createElement('a')

            span.id = `tag${tag.id}`
            span.classList.add('course__tag')

            if (index % 3 == 0) {
                span.style.backgroundColor = 'rgb(208,162,200,60%)'
            } else if (index % 2 == 0) {
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
                    <i class="fa-solid fa-heart heart" style="${article.liked_for_this_user ? 'color: #EAB6E1': 'color: #202020'}"></i>
                    <span>${article.likes_count}</span>
                </div>
                <div>
                    <i class="fa-solid fa-message comment"></i>
                    <span>${article.comments_count}</span>
                </div>
            </div>
            <div class='course__footer__right'>
                
            </div>
        </div>
        `

        return div
    }

    showAllCourses.addEventListener('click', (e) => {
        if (e.target.classList.contains('heart')) {
            //
            let article = e.target.parentNode.parentNode.parentNode.parentNode;

            fetch(`/api/article/article-list/${article.id}/likes`, {
                method: 'POST',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        let heart = e.target
                        let span = heart.parentNode.querySelector('span')

                        if (data.message === 'Like removed successfully!') {
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
            let article = e.target.parentNode.parentNode
            let menu = article.querySelector('.course__header__options')

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

    const renderSelectTags = async (select) => {
        const response = await fetch('/api/tags')
        const data = await response.json()

        if (data.status === 'success') {
            data.tags.forEach(tag => {
                const option = document.createElement('option')
                option.value = tag.id
                option.innerHTML = tag.name
                select.appendChild(option)
            })
        }
    }

    const createArticleFilters = (place) => {
        const select = document.createElement('select')
        const tags_select = document.createElement('select')

        select.name = 'sort_by'
        tags_select.name = 'tags'

        select.id = 'SortedBy'
        tags_select.id = 'TagsFilter'
        tags_select.multiple = true

        const option_values = ['Newest', 'Oldest', 'Popular', 'Unpopular']
        option_values.forEach((option, index) => {
            const element = document.createElement('option')
            element.value = option
            element.innerHTML = option
            select.appendChild(element)
        })

        const tags_all_option = document.createElement('option')
        tags_all_option.value = ''
        tags_all_option.innerHTML = 'All'
        tags_select.appendChild(tags_all_option)

        renderSelectTags(tags_select)

        select.addEventListener('change', () => sendFilters(searchForm.querySelector('input'),
            select, tags_select))
        tags_select.addEventListener('change', () => sendFilters(searchForm.querySelector('input'),
            select, tags_select))

        place.appendChild(select)
        place.appendChild(tags_select)
    }

    function sendFilters(search, select, tags_select) {
        console.log(search, select, tags_select)
        const selectedTagOptions = Array.from(tags_select.selectedOptions);
        const selectedTagValues = selectedTagOptions.map(option => option.value);
        const selectedSortOption = select.selectedOptions[0].value
        const q = search.value
        getAllArticles(q, selectedSortOption, selectedTagValues)
    }

    if (searchForm.querySelector('input')) {
        const input = searchForm.querySelector('input')

        searchForm.addEventListener('submit', (e) => {
            e.preventDefault()
            sendFilters(input, showFilters.querySelector('#SortedBy'),
                showFilters.querySelector('#TagsFilter'))
        })

        input.addEventListener('input', (e) => {
              e.preventDefault()
              if (input.value.length > 1) {
                sendFilters(input, showFilters.querySelector('#SortedBy'),
                        showFilters.querySelector('#TagsFilter'))
              }
        })
    }


    createArticleFilters(showFilters)

    showHideElement(filtersButton, showFilters)
    showHideElementShow(showFilters)
})
