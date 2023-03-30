from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Article, ArticleComment
from course.models import Tag

from .services import get_all_articles, get_one_article, get_all_tags, article_comments_filter, articles_list_filter_tags, article_get_one_comment
from .utils import slug_generator


def articleList(request):
    # Get all articles and tags
    articles = get_all_articles()
    tags = get_all_tags()

    public_articles = []
    
    # Articles Filter
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    articles = Article.objects.filter(tag__name__icontains=q)
    
    for article in articles:
        if article.public == True:
            public_articles.append(article)
            
    context = {
        'articles': public_articles,
        'tags': tags
    }
    return render(request, 'article/articleList.html', context)

def createArticle(request):
    page = 'create_article'

    # get all tags and articles
    articles = get_all_articles()
    tags = get_all_tags()
    
    # create new article
    if request.method == 'POST':
        # get data from form
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        text = request.POST.get('text')
        public = request.POST.get('public')
        
        # generate slug
        slug = slug_generator(title)
        user = request.user
        
        # check public status
        if public == 'on': 
            public = True
        elif public == None:
            public = False

        # check text, tag and title     
        if len(text) < 10:
            messages.error(request, 'Text must be at least 10 characters')
        if (tag == None ):
            messages.error(request, 'Tag must be selected')
        if len(title) < 4:
            messages.error(request, 'Title must be at least 4 characters')
        
        # check if article already exists
        for article in articles:
            if slug == article.slug:
                messages.error(request, 'This article already exists')
                
        # get tag object
        tag = Tag.objects.get(id = tag)
                
        # create new article
        form = Article.objects.create(
            user = user,
            title = title,
            slug = slug,
            tag = tag,
            text = text,
            public = public,
        )
        
        form.save()
        return redirect('/articles')
                    
    context = {
        'tags': tags,
        'page': page,
    }
    return render(request, 'article/createArticle.html', context)


def showArticle(request, slug):
    # get article and comments
    article = get_one_article(slug)
    comments = article_comments_filter(article)

    # articles list filter
    articles = get_all_articles()
    articles_filters = articles_list_filter_tags(article.tag)

    latest_articles = []
    public_articles = []

    user = request.user
    
    #filter Articles
    for a in articles:
        if article.title != a.title:
            latest_articles.append(a)
            
    #Also Filter Articles
    for i in articles_filters: 
        if article.title != i.title:
            public_articles.append(i)
            
    # Likes

    liked = False

    likes = article.likesForArticle
    likes_count = (article.likesForArticle).count()

    for like in likes.all(): 
        if like.username == request.user.username:
            print(like.username)
            liked = True
            
    if request.method == 'POST':
        type = request.POST.get('type')
        
        # add new like or remove old like
        if type == 'like':
            if request.user.is_authenticated: 
                status = False
                
                # get status
                for like in likes.all(): 
                    if like.username == request.user.username:
                        status = True
                        print(like.username)
                
                # check if user already liked
                if status:
                    # if liked, remove like
                    liked = False
                    article.likesForArticle.remove(like)

                if status == False:
                    # if not liked, add like
                    liked = True
                    article.likesForArticle.add(request.user)

                    article.save()

                return redirect('/articles/'+ slug+'/#like')
            else:
                return redirect('/sign-in')
            
        # create new comments
        if type == 'comment':
            if request.user.is_authenticated:
                # get data from form
                message = request.POST.get('message')
                
                # check data 
                if len(message) < 6:
                    messages.error(request, 'Message is too short')
                
                # create new comment
                form = ArticleComment.objects.create(
                    article=article,
                    user=user,
                    message=message,
                )

                form.save()
                return redirect('/articles/'+ slug+'#comments')
            else:
                return redirect('base:login')
                        
    context =  {
        'article': article, 
        'articles': latest_articles[:4], 
        'tag_articles': public_articles[:4], 
        'likes': likes_count,
        'liked': liked,
        'comments': comments
    }
    return render(request, 'article/showArticle.html', context)


def deleteComment(request,slug, id):
    if request.user.is_authenticated:
     # get comment
        comment = article_get_one_comment(id)
        
        # check comment and user
        if comment:
            if comment.user == request.user:
                #delete comment
                comment.delete()
            else:
                messages.error(request, 'You are not allowed to delete this comment')
        else:
            messages.error(request, 'Comment not found')
        
        return redirect('/articles/'+ slug+'/#comments')
    else:
        return redirect('base:registration')


def updateArticle(request, slug):
    page = 'update_article'

    # get article and all articles and tags
    article = get_one_article(slug)
    articles = get_all_articles()
    tags = get_all_tags()
    
    if request.method == 'POST':
        # get data from form
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        text = request.POST.get('text')
        public = request.POST.get('public')
                
        # check public status
        if public == 'on': 
            public = True
        elif public == None:
            public = False
            
        # check text, tag and title
        if len(text) < 10:
            messages.error(request, 'Text must be at least 10 characters')
        if (tag == None ):
            messages.error(request, 'Tag must be selected')
        if len(title) < 4:
            messages.error(request, 'Title must be at least 4 characters')
            
        # if (int(article.tag.id)) != int(tag):
        tag = Tag.objects.get(id = tag)    
            
        # update article data
        article.title = title
        article.tag = tag
        article.text = text
        article.public = public
        
        article.save()
        return redirect('/articles')
        
    context = {
        'article': article,
        'tags': tags,
        'page': page, 
    }
    return render(request, 'article/createArticle.html', context)


def deleteArticle(request, slug):
    if request.user.is_superuser:
     # get article
        article = get_one_article(slug)
        
        # check article and user
        if article:
            if article.user == request.user:
                #delete article
                article.delete()
            else:
                messages.error(request, 'You are not allowed to delete this article')
        else:
            messages.error(request, 'Article not found')
        
        return redirect('/articles/'+ slug)
    else:
        return redirect('base:registration')

