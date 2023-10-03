from django.contrib import admin
from .models import Task, Course 
# Register your models here.

admin.site.register(Course)
admin.site.register(Task)