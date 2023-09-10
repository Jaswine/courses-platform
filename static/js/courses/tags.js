document.addEventListener('DOMContentLoaded', () => {
    const ShowAllTags = document.querySelector('#ShowAllTags')
    const form = document.querySelector('#CreateTagForm')

    const getAllTags = () => {
        fetch('/api/tags')
            .then((response) => response.json())
            .then(data => {
                ShowAllTags.innerHTML = ''

                if (data.tags.length > 0) {
                    data.tags.forEach(tag => {
                        const div = document.createElement('div')

                        div.id = tag.id
                        div.classList.add('tag')

                        div.innerHTML = `
                            <h3>${tag.name}</h3>
                            <span class="material-symbols-outlined close__tag">
                                close
                            </span>
                        `

                        ShowAllTags.appendChild(div)
                    });
                } else {
                    ShowAllTags.innerHTML = 'Tags not found'
                }
            })
            .catch((error) => {
                console.log(error)
            })
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault()
        
        let data = new FormData(form)
        fetch('/api/tags', {
            method: 'POST',
            body: data
        }) 
            .then((response) => response.json())
            .then(data => {
                getAllTags()
                form.querySelector('.name').value = ''
            })
            .catch((error) => {
                console.log(error)
            })
    })

    ShowAllTags.addEventListener('click', (e) => {
        if (e.target.classList.contains('material-symbols-outlined')) {
            let tag = e.target.parentNode

            fetch(`/api/tags/${tag.id}`, {
                method: 'DELETE',
            }) 
                .then((response) => response.json())
                .then(data => {
                    getAllTags()
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    })

    getAllTags()
})