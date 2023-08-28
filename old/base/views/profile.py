from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
import random
from django.contrib.auth.decorators import login_required
from requests import get

from django.contrib.auth.models import User
from course.models import  Tag, Course, CourseTask
from ..models import Profile
from article.models import Article, ArticleComment

from ..services import get_filter_courses, get_filter_articles, user_filter_profile, get_user, get_user_profile, get_all_courses
from article.services import get_all_tags, get_all_articles
from ..forms import UpdateProfileForm, UpdateUserForm


def profile(request, username):
   page='profile'

   #get user and profile
   user = get_user(username)
   profile = get_user_profile(user)
   
   # if user doesn't have image
   ProfileImage = 'https://images.pexels.com/photos/4587958/pexels-photo-4587958.jpeg?auto=compress&cs=tinysrgb&w=800'
   
   context = {
      'user': user, 
      'page': page, 
      'profile': profile, 
      'ProfileImage': ProfileImage,
   }
   return render(request,'base/profile/profile.html', context)

#Courses
# For admin user
def profile_courses_view(request, username):
    page='courses'

    # get user and profile
    user = get_user(username)
    profile = get_user_profile(user)
    
    # get user courses
    courses = Course.objects.filter(user=user)
    
    context = {
        'user': user,  
        'page':page, 
        'profile': profile, 
        'courses': courses
    }
    return render(request,'base/profile/profile.html', context)
 
#Articles 
#for admin user
def profile_articles_view(request, username):
    page = 'articles'
    
    # get user and profile
    user = get_user(username=username)
    profile = Profile.objects.get(user=user)

    # get user articles
    articles = Article.objects.filter(user=user)
    
    context = {
        'page': page, 
        
        'user': user,  
        'profile': profile,
        
        'articles': articles, 
    }
    return render(request,'base/profile/profile.html', context)
 
 #Articles 
#for admin user
def profile_sertificates(request, username):
    page = 'sertificates'
    
    # get user and profile
    user = get_user(username=username)
    profile = Profile.objects.get(user=user)

    
    context = {
        'page': page, 
        
        'user': user,  
        'profile': profile,
    }
    return render(request,'base/profile/profile.html', context)
 
# FOR AUTH USER
# liked courses and articles
def profile_likes_view(request, username):
    page = 'like'

    # get user and profile
    user = get_user(username)
    profile = get_user_profile(user)
    
    articles = get_all_articles()
    courses = get_all_courses()
    
    # articles and courses sorting
    like_articles = []
    liked_courses = []

    status_for_courses = False
    status = False
    
    # articles filter
    for article in articles:
        for like in article.likesForArticle.all():
            if like.username == user.username:
                like_articles.append(article)
                if request.user.username == like.username:
                    status = True

    # courses filter
    for course in courses:
        for like in course.likes.all():
            if like.username == user.username:
                liked_courses.append(course)
                if request.user.username == like.username:
                    status = True
    
    context = {
        'user': user,  
        'page': page, 
        'like_articles': like_articles, 
        'profile': profile, 
        'status': status,
        'status_for_courses': status_for_courses,
        'liked_courses': liked_courses,
    }
    return render(request,'base/profile/profile.html', context)
 
#FOR AUTH USER
@login_required(login_url='base:login')
def profile_update_view(request, username):
    page = 'update_profile'
    # get user and profile
    user = get_user(username=username)
    profile = get_user_profile(user)
    
    profile_form = UpdateProfileForm(instance=profile)
    user_form = UpdateUserForm(instance=user)
    
    # user and profile checking 
    if request.method == 'POST':
      profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
      user_form = UpdateUserForm(request.POST,instance=user)

      if user_form.is_valid():
         if profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/profile/'+request.user.username)
    
    context = {
       'page': page, 
       
       'user': user, 
       'profile': profile,
       
       'profile_form': profile_form,
       'user_form': user_form
      }
    return render(request,'base/profile/profile.html', context)

