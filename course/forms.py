from django.forms import ModelForm
from .models import Course, Tag, Task

class CourseForm(ModelForm):
   class Meta:
      model = Course
      fields = [
                'title', 
                'image',
                'tags',
                'about',
                'level', 
                'public',
            ]
      
class TaskForm(ModelForm):
   class Meta:
      model = Task
      fields = [
               'title', 
               'text',
            ]
      
      