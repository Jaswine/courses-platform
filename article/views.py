from django.shortcuts import render, redirect
from .models import Article, ArticleComment
from course.models import Tag
from django.contrib import messages

def articleList(request):
    articles = Article.objects.all()
    public_articles = []
    
    for article in articles:
        if article.public == True:
            public_articles.append(article)
            
    print(request.user.username)
    
    context = {'articles': public_articles}
    return render(request, 'article/articleList.html', context)

def createArticle(request):
    tags = Tag.objects.all()
    articles = Article.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        text = request.POST.get('text')
        public = request.POST.get('public')
        
        slug = '-'.join(title.lower().split(' '))
        user = request.user
        
        if public == 'on': #! PUBLIC & UNPUBLIC
            public = True
        elif public == None:
            public = False
                
        if len(text) < 10: #! VALIDATION
            messages.error(request, 'Text must be at least 10 characters')
        if (tag == None ):
            messages.error(request, 'Tag must be selected')
        if len(title) < 4:
            messages.error(request, 'Title must be at least 4 characters')
        for article in articles:
            if slug == article.slug:
                messages.error(request, 'This article already exists')
                
        tag = Tag.objects.get(id = tag)
                
        form = Article.objects.create( #! CREATE ARTICLE
            user = user,
            title = title,
            slug = slug,
            tag = tag,
            text = text,
            public = public,
        )
        print(form)
        
        form.save()
        return redirect('/articles')
                    
    context = {'tags': tags}
    return render(request, 'article/createArticle.html', context)

def showArticle(request, slug):
    article = Article.objects.get(slug = slug)
    comments = ArticleComment.objects.filter(article=article)
    user = request.user
    
    articles = Article.objects.all()
    articles_filters = Article.objects.filter(tag = article.tag)
    latest_articles = []
    public_articles = []
    
    for a in articles: #filter Articles
        if article.title != a.title:
            latest_articles.append(a)
            
    for i in articles_filters: #Also Filter Articles
        if article.title != i.title:
            public_articles.append(i)
            
    #* Likes
    likes = article.likesForArticle
    likes_count = (article.likesForArticle).count()
            
    if request.user.is_authenticated:
        if request.method == 'POST':
            type = request.POST.get('type')
            
            if type == 'like':
                status = False
                
                for like in likes.all(): 
                    if like.username == request.user.username:
                        status = True
                        print(like.username)
                
                if status == True:
                    article.likesForArticle.remove(like)
                if status == False:
                    article.likesForArticle.add(request.user)
                    article.save()
                        
                return redirect('/articles/'+ slug+'/#like')
            if type == 'comment':
                message = request.POST.get('message')
                print(message)
                
                if len(message) < 3:
                    return messages.error(request, 'Message is too short')
                    
                
                form = ArticleComment.objects.create(
                    article=article,
                    user=user,
                    message=message,
                )
                form.save()
                return redirect('/articles/'+ slug+'/#comments')
            
    context =  {
        'article': article, 
        'articles': latest_articles[:4], 
        'tag_articles': public_articles[:4], 
        'likes': likes_count,
        'comments': comments
    }
    return render(request, 'article/showArticle.html', context)

def deleteComment(request,slug, id):
    comment =  ArticleComment.objects.get(id=id)
    comment.delete()
    return redirect('/articles/'+ slug+'/#comments')

def updateArticle(request, slug):
    article = Article.objects.get(slug = slug)
    articles = Article.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        text = request.POST.get('text')
        public = request.POST.get('public')
                
        if public == 'on': #! PUBLIC & UNPUBLIC
            public = True
        elif public == None:
            public = False
            
        if len(text) < 10: #! VALIDATION
            messages.error(request, 'Text must be at least 10 characters')
        if (tag == None ):
            messages.error(request, 'Tag must be selected')
        if len(title) < 4:
            messages.error(request, 'Title must be at least 4 characters')
            
        # if (int(article.tag.id)) != int(tag):
        tag = Tag.objects.get(id = tag)    
            
        article.title = title
        article.tag = tag
        article.text = text
        article.public = public
        
        article.save()
        return redirect('/articles')
        
    context = {'article': article, 'tags': tags}
    return render(request, 'article/updateArticle.html', context)

def deleteArticle(request, slug):
    article = Article.objects.get(slug = slug)
    
    if request.method == 'POST':
        article.delete()
        redirect('/articles')

    return render(request, 'article/deleteArticle.html', {'article': article})



    