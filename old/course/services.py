from .models import Tag, CourseTitle, Course, CourseTask


def course_filter():
   return Course.objects.filter(public=True)

def get_one_course(slug):
   return Course.objects.get(slug=slug)

def get_one_task(pk):
   return CourseTask.objects.get(id=pk)
