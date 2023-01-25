from django.contrib import admin
# from .models import Course, CourseComment, CourseTitle, CourseVideo,  CourseVideoComment, WriteCode, WriteCodeComment, Question, CodeTest, CodeTestComment
from .models  import Course, CourseComment, CourseTitle, CourseTask, Tag, CourseReview


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'updated')
    
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'message')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'user', 'stars', 'message')

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(CourseTitle)
admin.site.register(CourseTask)
admin.site.register(Tag, TagAdmin)
admin.site.register(CourseReview, CourseReviewAdmin)