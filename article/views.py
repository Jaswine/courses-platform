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
    
    print(len(public_articles))
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