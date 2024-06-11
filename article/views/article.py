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


def create_article(request):
    """
        Создание статьи
    """
    if request.user.is_authenticated:
        form = ArticleForm()

        if request.method == 'POST':
            form = ArticleForm(request.POST)

            if form.is_valid():
                article = form.save(commit=False)
                article.user = request.user
                article.save()

                return redirect('article:article_list')

        return render(request, 'article/article_form.html', {
            'form': form,
        })
    else:
        return redirect('dashboard')


def article_detail(request, id: int):
    """
        Вывод одной статьи
    """
    article = get_object_or_404(Article, pk=id)

    return render(request, 'article/article.html', {
        'article': article,
    })


def update_article(request, id: int):
    """
        Обновление статьи
    """
    article = get_object_or_404(Article, pk=id)
    form = ArticleForm(instance=article)

    return render(request, 'article/article_form.html', {
        'form': form,
    })


def delete_article(request, id: int):
    """
        Удаление статьи
    """
    article = get_object_or_404(Article, pk=id)

    return render(request, 'article/article_delete.html', {
        'article': article,
    })
