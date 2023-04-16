from modeltranslation.translator import register, TranslationOptions

from .models import Article, ArticleComment 

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
 fields = ('title', 'text')
 
@register(ArticleComment)
class ArticleCommentTranslationOptions(TranslationOptions):
 fields = ('article', 'message')