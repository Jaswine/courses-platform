from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from article.models import Article
from article.forms import ArticleForm
from article.services.article_form_service import delete_article, update_article, create_article
from course.services.tag_service import get_all_tags


def article_list_view(request):
    """
        Вывод всех статей
    """
    context = {
        'tags': get_all_tags(),
    }
    return render(request,
                  'article/article_list.html',
                  context)


@login_required(login_url='auth:sign-in')
def create_article_view(request):
    """
        Создание статьи
    """
    if request.user.is_superuser:
        form = ArticleForm()

        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            article = create_article(form, request.user)

            if article:
                return redirect('article:article_list')
            messages.error(request, 'Article creation error')
            return redirect('article:create_article')

        return render(request,
                      'article/article_form.html',
                      {
                        'status': 'Create',
                        'form': form,
                      })

    return redirect('article:article_list')


def article_detail_view(request, id: int):
    """
        Вывод одной статьи
    """
    article = get_object_or_404(Article, pk=id)

    return render(request, 'article/article.html', {
        'article': article,
    })


@login_required(login_url='auth:sign-in')
def update_article_view(request, id: int):
    """
        Обновление статьи
    """
    if request.user.is_superuser:
        article = get_object_or_404(Article, pk=id)
        form = ArticleForm(instance=article)

        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            article = update_article(form)

            if article:
                messages.success(request, 'The article has been updated successfully!')
                return redirect('article:article_list')
            messages.error(request, 'Article update error')

        return render(request, 'article/article_form.html', {
            'status': 'Update',
            'article': article,
            'form': form,
        })

    return redirect('article:article_list')


@login_required(login_url='auth:sign-in')
def delete_article_view(request, id: int):
    """
        Удаление статьи
    """
    article = get_object_or_404(Article, pk=id)

    if request.method == 'POST':
        delete_article(article)

        messages.success(request, 'Article deleted successfully!')
        return redirect('article:article_list')

    return render(request, 'article/article_delete.html', {
        'article': article,
    })
