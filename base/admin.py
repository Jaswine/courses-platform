from django.contrib import admin
from .models import Tag, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )

admin.site.register(Tag)
admin.site.register(Profile, ProfileAdmin)