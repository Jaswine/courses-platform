from django.shortcuts import render, redirect
from .models import Article, ArticleComment
from base.models import Tag
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
    
    articles = Article.objects.all()
    articles_filters = Article.objects.filter(tag = article.tag)
    latest_articles = []
    public_articles = []
    
    for a in articles:
        if article.title != a.title:
            latest_articles.append(a)
            
    for i in articles_filters:
        if article.title != i.title:
            public_articles.append(i)
            
    context =  {'article': article, 'articles': latest_articles[:4], 'tag_articles': public_articles[:4]}
    return render(request, 'article/showArticle.html', context)

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
            
        if (int(article.tag.id)) != int(tag):
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