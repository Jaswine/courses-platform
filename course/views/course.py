from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

# models
from ..models import Tag, Course

from ..forms import CourseForm

# services
from base.services import get_all_courses
from article.services import get_all_tags

# utils
from article.utils import checking_slug, slug_generator

def show_all_courses_view(request):
    # get all courses
    courses = Course.objects.all()
    
    context = {
        'courses': courses
    }
    return render(request, 'course/showAllCourses.html', context)

def course(request, slug):
    # get course and titles
    course = Course.objects.get(slug=slug)
                
    context = {
        'course': course, 
    }
    return render(request, 'course/CourseInfo.html', context)
 
@login_required(login_url='base:login')
def create_course_view(request):
    if request.user.is_superuser:
        form = CourseForm()
       
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
           
            if form.is_valid():
                slug = checking_slug(slug_generator(form.cleaned_data.get('title')))
                
                course = form.save(commit=False)
                course.user = request.user
                course.slug = slug
            
                form.save()
                return redirect('/profile/'+str(request.user.username)+'/courses')
            
        return render(request, 'course/AddNewCourse.html', { 'form': form})
    else:
        return redirect('base:registration')
    
@login_required(login_url='base:login')
def delete_course(request, slug):
   if request.user.is_superuser:
     # get article
        course = Course.objects.get(slug=slug)
        
        # check article and user
        if request.method == 'POST':
            if course.user.username == request.user.username:
                #delete article
                course.delete()
                return redirect('course:show_all_courses')
            else:
                messages.error(request, 'You are not allowed to delete this article')
        
        context = {
           'course': course
        }
        return render(request, 'course/DeleteCourse.html', context)
   else:
        return redirect('article:registration')
