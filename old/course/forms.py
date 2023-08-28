from django.forms import ModelForm
from .models import Course, CourseTask

class CourseForm(ModelForm):
   class Meta:
      model = Course
      fields = ['title', 'image', 'tags', 'about', 'whatAreUWillLearn', 'level', 'initialRequirements', 'certificate', 'public']
      
class TaskForm(ModelForm):
   class Meta:
      model = CourseTask
      fields = ['title', 'description']
   
class TaskForm(ModelForm):
   class Meta:
      model = CourseTask
      fields = ['title', 'description']