from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Article, ArticleComment
from course.models import Tag
from .forms import ArticleForm

from .services import get_all_articles, get_one_article, get_all_tags, article_comments_filter, articles_list_filter_tags, article_get_one_comment
from .utils import slug_generator, checking_slug


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
            slug = checking_slug(slug_generator(form.cleaned_data.get('title')))
            
            article = form.save(commit=False)
            article.user = request.user
            article.slug = slug
         
            article.save()
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
   
   filtered_articles = Article.objects.filter(tag=article.tag)
   last_articles = get_all_articles()
   
   liked = False

   likes = article.likesForArticle
   likes_count = (article.likesForArticle).count()
   
   user = request.user

   for like in likes.all(): 
      if like.username == request.user.username:
         liked = True

   if request.method == 'POST':
      type = request.POST.get('type')
      
      if request.user.is_authenticated == False: 
         return redirect('/login')
         
      if type == 'like':
         status = False
         
         for like in likes.all(): 
            if like.username == request.user.username:
               status = True
         
         if status:
            liked = False
            article.likesForArticle.remove(like)

         if status == False:
            liked = True
            article.likesForArticle.add(request.user)

            article.save()

         return redirect('/articles/'+ slug)

         
      # create new comments
      if type == 'comment':
         message = request.POST.get('message')
         
         if len(message) < 6:
            messages.error(request, 'Message is too short')
         
         form = ArticleComment.objects.create(
            article=article,
            user=user,
            message=message,
         )

         form.save()
         return redirect('/articles/'+ slug)
    
   context =  {
      'article': article,
      'comments': comments,
      
      'liked': liked,
      'filtered_articles': filtered_articles[3:],
      'last_articles': last_articles[3:]
   }
   return render(request, 'article/showOneArticle.html', context)

@login_required(login_url='base:login')
def delete_comment(request,slug, id):
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
      
      return redirect('/articles/'+ slug)
    else:
        return redirect('base:registration')

@login_required(login_url='base:login')
def update_article(request, slug):
   if request.user.is_superuser:
      article = get_one_article(slug)
      page_type = 'update_article'
      
      if article.user == request.user:
         form = ArticleForm(instance=article)
      
         if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            
            if form.is_valid():
               form.save()
               return redirect('article:all_articles')
         
         context = {
            'page_type': page_type,
            'form': form,
            'article': article
         }
         return render(request, 'article/CreateUpdateArticle.html', context)
      else: 
         redirect('article:all_articles')
   else:
      messages.error(request, 'You are not allowed to edit this article')
      return redirect('article:all_articles')
   

@login_required(login_url='base:login')
def delete_article(request, slug):
   if request.user.is_superuser:
     # get article
        article = get_one_article(slug)
        
        # check article and user
        if article:
           if request.method == 'POST':
               if article.user == request.user:
                  #delete article
                  article.delete()
                  return redirect('article:all_articles')
               else:
                  messages.error(request, 'You are not allowed to delete this article')
        else:
            messages.error(request, 'Article not found')
        
        context = {
           'article': article
        }
        return render(request, 'article/DeleteArticle.html', context)
   else:
        return redirect('article:registration')
