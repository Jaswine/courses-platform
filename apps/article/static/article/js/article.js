document.addEventListener('DOMContentLoaded', () => {
    const ArticleCommentsForm = document.querySelector('#ArticleCommentsForm')
    const ArticleComments = document.querySelector('#ArticleComments')
    const articleId = document.querySelector('#ArticleID')

    const getArticleComments = async () => {
        const response = await fetch(`/api/article/article-list/${articleId.value}/comments`)
        const data = await response.json()

        if (response.status === 200) {
            console.log('DATA: ', data)
            renderComments(data.comments)
        }
    }

    const renderComments = (comments) => {
        ArticleComments.innerHTML = ''
        if (comments.length > 0) {
            comments.forEach((comment, index) => {

            })
        } else {
            ArticleComments.innerHTML = `
                <div class='comments__not__found'>
                    <h2>Comments not found 🔎</h2>
                </div>
            `
        }
    }

    getArticleComments()
})