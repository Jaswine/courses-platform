from django.forms import ModelForm
from .models import Course, Tag

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
      
      