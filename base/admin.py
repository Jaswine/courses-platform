from django.contrib import admin
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Tag, TagAdmin)
# admin.site.register(Profile, ProfileAdmin)