from .models import Tag, CourseTitle, Course, CourseComment, CourseTask


def course_filter():
   return Course.objects.filter(public=True)

def get_one_course(slug):
   return Course.objects.get(slug=slug)

def course_title_filter(id):
   return CourseTitle.objects.filter(course=id)

def course_get_comments(course, commentType):
   return CourseComment.objects.filter(course=course,commentType = commentType)

def get_one_comment(id):
   return CourseComment.objects.get(id=id)

def get_one_task(pk):
   return CourseTask.objects.get(id=pk)

def get_all_exercises_from_titles(titles):
   tasks = []

   for title in titles:
        for exercise in  title.tasks.all().reverse():
            tasks.append(exercise)  
   
   return tasks