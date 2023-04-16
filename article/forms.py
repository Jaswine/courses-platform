from django.forms import ModelForm
from .models import Article
from ckeditor.fields import RichTextField

class ArticleForm(ModelForm):   
   class Meta:
      model = Article
      fields = ['title', 'tag', 'text', 'public']