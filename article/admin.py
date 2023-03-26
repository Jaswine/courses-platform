from django.contrib import admin

from .models import Article, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user' , 'tag', 'updated')
    
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'message', 'created')


# register models in admin panel
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
