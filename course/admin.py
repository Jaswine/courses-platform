from django.contrib import admin
from .models import Task, Course, TaskComment, TaskCommentUserComplaint

# Register your models here.

admin.site.register(Course)
admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(TaskCommentUserComplaint)