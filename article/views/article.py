from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from article.models import Article
from article.forms import ArticleForm
from course.models import Tag


def article_list(request):
    """
        Вывод всех статей
    """
    tags = Tag.objects.all()

    return render(request, 'article/article_list.html', {
        'tags': tags,
    })


@login_required(login_url='auth:sign-in')
def create_article(request):
    """
        Создание статьи
    """
    if request.user.is_authenticated:
        form = ArticleForm()

        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)

            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()

                return redirect('article:article_list')

        return render(request, 'article/article_form.html', {
            'status': 'Create',
            'form': form,
        })

    return redirect('article:article_list')


def article_detail(request, id: int):
    """
        Вывод одной статьи
    """
    article = get_object_or_404(Article, pk=id)

    return render(request, 'article/article.html', {
        'article': article,
    })


@login_required(login_url='auth:sign-in')
def update_article(request, id: int):
    """
        Обновление статьи
    """
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=id)
        form = ArticleForm(instance=article)

        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)

            if form.is_valid():
                form.save()

                return redirect('article:article_list')

        return render(request, 'article/article_form.html', {
            'article': article,
            'status': 'Update',
            'form': form,
        })

    return redirect('article:article_list')


@login_required(login_url='auth:sign-in')
def delete_article(request, id: int):
    """
        Удаление статьи
    """
    article = get_object_or_404(Article, pk=id)

    if request.method == 'POST':
        article.delete()

        messages.success(request, 'Article deleted successfully!')
        return redirect('article:article_list')

    return render(request, 'article/article_delete.html', {
        'article': article,
    })
