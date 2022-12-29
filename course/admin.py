from django.contrib import admin
# from .models import Course, CourseComment, CourseTitle, CourseVideo,  CourseVideoComment, WriteCode, WriteCodeComment, Question, CodeTest, CodeTestComment
from .models  import Course, CourseComment, CourseTitle, CourseTask


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'updated')
    
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'message')


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseComment, CourseCommentAdmin)
admin.site.register(CourseTitle)
admin.site.register(CourseTask)
# admin.site.register(CourseVideo)
# admin.site.register(CourseVideoComment)
# admin.site.register(WriteCode)
# admin.site.register(WriteCodeComment)
# admin.site.register(Question)
# admin.site.register(CodeTest)
# admin.site.register(CodeTestComment)