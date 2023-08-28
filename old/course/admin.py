from django.contrib import admin
from .models import Tag, TaskComment, Course, CourseTask, CourseReview, CourseTitle

admin.site.register(Tag)

admin.site.register(Course)
admin.site.register(CourseReview)

admin.site.register(CourseTitle)

admin.site.register(CourseTask)
admin.site.register(TaskComment)

