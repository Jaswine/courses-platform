from django.forms import ModelForm, CheckboxSelectMultiple

from article.models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'tags', 'is_published')
        widgets = {
            'tags': CheckboxSelectMultiple,
        }


