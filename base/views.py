from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
import random
from requests import get

from django.contrib.auth.models import User
from course.models import  Tag, Course, CourseTask
from .models import Profile
from article.models import Article, ArticleComment

from .services import get_filter_courses, get_filter_articles, user_filter_profile, get_user, get_user_profile, get_all_courses
from article.services import get_all_tags, get_all_articles


def home(request):
    # get data
    courses = get_filter_courses()
    articles = get_filter_articles()
    
    context = {
        'courses': courses, 
        'articles': articles
    }
    return render(request, 'base/Home.html', context)

def registration(request):
    if request.method == 'POST':
        # get data from form
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        # cheking on exits
        if User.objects.filter(username=name).count() == 0:
            if User.objects.filter(email=email).count() == 0: 
                # Checking validation
                if len(password) > 8:         
                    user = User.objects.create_user(name, email, password)
                    if user:
                        user.save()
                        
                        profile = Profile.objects.create(
                            user = user,
                        )

                        profile.save()

                        # login
                        login(request, user)
                        return redirect('/')        
                else:
                    messages.error(request, 'Password is too short')
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')       
                  
    return render(request,'base/Registration.html')

def loginUser(request):
    if request.method == 'POST':
        # get data from form
        email = request.POST.get('email')
        password = request.POST['password']
            
        # user cheking on exits
        try:
            user = User.objects.get(username=email)
        except: 
            messages.error(request, 'Username not found...')
            
        # user authentication
        user = authenticate(username=email, password=password)
        
        if user is not None:
            # login
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Password incorrect')   
        
    return render(request,'base/Login.html')


def logoutUser(request):
    # user logout
    logout(request)
    return redirect('/')


def listTags(request):
    # all tags
    tags  = get_all_tags()
    
    if request.user.is_superuser:
        if request.method == 'POST':
            # get data from form
            tag = request.POST.get('tag')
            
            # create new tag
            tagForm = Tag.objects.create(name=tag)

            tagForm.save()
    else:
        return redirect('/')
    
        
    context = {
        'tags': tags.reverse(), 
        'user': request.user
    }
    return render(request,'base/Tags.html', context)


def deleteTag(request, id):
    if  request.user.is_superuser:
        # get tag
        tag = Tag.objects.get(id=id)

        if tag:
            # delete tag
            tag.delete()
        else:
            messages.error(request, 'Tag not found')
        
        return redirect('/tags')
    else:
        return redirect('/')

def profile(request, username):
    page='profile'

    #get user and profile
    user = get_user(username)
    profile = get_user_profile(user)
    
    # if user doesn't have image
    ProfileImage = 'https://images.pexels.com/photos/4587958/pexels-photo-4587958.jpeg?auto=compress&cs=tinysrgb&w=800'
    getPhoto = []
        
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': '563492ad6f91700001000001cc06828fc3ab4e418257550da9b440d7',
    }
    
    #TODO: Get a Photo for a Profile, If user doesn't have a photo
    try:
        response = get('https://api.pexels.com/v1/search?query=funny_cat&curated?page=1&per_page='+str(user.id), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
        if  data:
            getPhoto = data['photos']
            
            for i in getPhoto:
                getPhoto = i
            
            getPhoto = getPhoto['src']['small']
            print(getPhoto)
            
            ProfileImage = getPhoto
        else:
            ProfileImage = 'https://images.pexels.com/photos/4587958/pexels-photo-4587958.jpeg?auto=compress&cs=tinysrgb&w=800'
            print('Response error: %s' % response.status_code)
    except:
        print('Pexels not found, Internet is broken!')
        messages.error(request, 'Internet is broken!   /(X_X)/ ')
    
    context = {'user': user, 'page': page, 'profile': profile, 'ProfileImage': ProfileImage,'getPhoto': getPhoto}
    return render(request,'base/user/Profile.html', context)

#Courses
# For admin user
def profileCourses(request, username):
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
    return render(request,'base/user/Profile.html', context)

#Articles 
#for admin user
def profileArticles(request, username):
    page = 'articles'
    
    # get user and profile
    user = get_user(username=username)
    profile = Profile.objects.get(user=user)

    # get user articles
    articles = Article.objects.filter(user=user)
    
    context = {
        'user': user,  
        'page': page, 
        'articles': articles, 
        'profile': profile
    }
    return render(request,'base/user/Profile.html', context)

# FOR AUTH USER
# liked courses and articles
def profileLikes(request, username):
    page = 'likes'

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
    return render(request,'base/user/Profile.html', context)

#FOR AUTH USER
def profileUpdate(request, username):
    # get user and profile
    user = get_user(username=username)
    profile = get_user_profile(user)
    
    # user and profile checking 
    if user:
        if profile:
            if request.method == 'POST':
                # get data from form
                email = request.POST.get('email')
                
                profileImage = profile.image
                image = request.FILES.get('image',profileImage)
                location = request.POST.get('location')
                
                bio = request.POST.get('bio')
                
                number = request.POST.get('number')
                twitter = request.POST.get('twitter')
                github = request.POST.get('github')
                telegram = request.POST.get('telegram')
                website = request.POST.get('website')
                

                # update profile
                user.email = email
            
                profile.image = image
                profile.bio = bio
                
                profile.twitter = twitter
                profile.github = github
                profile.telegram = telegram
                profile.website = website
                profile.number = number
                profile.location = location
            
                user.save()
                profile.save()
                return redirect('/profile/'+request.user.username)
        else: 
            messages.add_message(request, 'Profile not found')
    else:
        messages.add_message(request, 'Profile not found')     
    
    context = {'user': user, 'profile': profile}
    return render(request,'base/user/ProfileUpdate.html', context)