from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Article, ArticleComment
from course.models import Tag
from .forms import ArticleForm

from .services import get_all_articles, get_one_article, get_all_tags, article_comments_filter, articles_list_filter_tags, article_get_one_comment


def get_all_articles_list(request):
   articles = get_all_articles()
   tags = get_all_tags()
   
   # Articles Filter
   q = request.GET.get('q') if request.GET.get('q') != None else ''
   articles = Article.objects.filter(tag__name__icontains=q)
   
   context = {
      'articles': articles,
      'tags': tags
   }
   return render(request, 'article/AllArticlesPage.html', context)

@login_required(login_url='base:login')
def create_article(request):
   if request.user.is_superuser:
      page_type = 'create_article'
      form  = ArticleForm()
      
      if request.method == 'POST':
         form = ArticleForm(request.POST)
         
         if form.is_valid():
            form.save(commit=false)
            form.user = request.user
            
            form.save()
            return redirect('article:all_articles')
         
      context = {
         'page_type': page_type,
         
         'form': form,
      }
      return render(request, 'article/CreateUpdateArticle.html', context)
   else:
      return redirect('article:all_articles')

def show_article(request, slug):
   article = get_one_article(slug)
   comments = article_comments_filter(article)
    
   context =  {
      'article': article,
      'comments': comments
   }
   return render(request, 'article/showOneArticle.html', context)


@login_required(login_url='base:login')
def update_article(request, slug):
   if request.user.is_superuser:
      article = get_one_article(slug)
      
      if article.user == request.user:
         form = ArticleForm(instance=article)
      
         if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            
            if form.is_valid():
               form.save()
               return redirect('base:all_articles')
         
         context = {
            'article': article
         }
         return render(request, 'article/CreateUpdateArticle.html', context)
      else: 
         redirect('article:all_articles')
   else:
      return redirect('article:all_articles')
   

@login_required(login_url='base:login')
def delete_article(request, slug):
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
