from django.shortcuts import render, redirect
from course.models import  Tag
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator
from .models import Profile
from article.models import Article, ArticleComment


def home(request):
    context = {}
    return render(request, 'base/Home.html', context)

#! _______________________AUTH_____________________
def registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        
        #! cheking on exits
        if User.objects.filter(username=name).count() == 0:
            if User.objects.filter(email=email).count() == 0: 
                #! Checking validation
                if len(password) > 8:         
                    user = User.objects.create_user(name, email, password)
                    if user:
                        user.save()
                        
                        profile = Profile.objects.create(
                            user = user,
                        )
                        profile.save()
                        
                        login(request, user)
                        return redirect('/')        
                else:
                    messages.error(request, 'Password is too short')
            else:
                messages.error(request, 'Email already exists')
        else:
            messages.error(request, 'Username already exists')       
                  
    context = {}
    return render(request,'base/Registration.html', context)

def loginUser(request):
    if request.method == 'POST':
        #?: get data
        email = request.POST.get('email')
        password = request.POST['password']
            
        try:
            user = User.objects.get(username=email)
        except: 
            messages.error(request, 'Username not found...')
            
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Password incorrect')   
        
    return render(request,'base/Login.html')

def logoutUser(request):
    logout(request)
    return redirect('/')


#! ________________TAGS_____________
def listTags(request):
    tags  = Tag.objects.all()
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == 'POST':
                tag = request.POST.get('tag')
                
                tagForm = Tag.objects.create(name=tag)
                tagForm.save()
                return redirect('/tags')
        else:
            return redirect('/')
    else:
        return redirect('/')
    
    tags = tags.reverse() 
        
    context = {'tags': tags, 'user': request.user}
    return render(request,'base/Tags.html', context)

def deleteTag(request, id):
    if request.user.is_authenticated:
        if  request.user.is_superuser:
            tag = Tag.objects.get(id=id)

            if tag:
                tag.delete()
            
            return redirect('/tags')
    return redirect('/')

def profile(request, username):
    page='profile'
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    
    context = {'user': user, 'page': page, 'profile': profile}
    return render(request,'base/user/Profile.html', context)

#Courses
# For admin user
def profileCourses(request, username):
    page='courses'
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    
    context = {'user': user,  'page':page, 'profile': profile}
    return render(request,'base/user/Profile.html', context)

#Articles 
#for admin user
def profileArticles(request, username):
    page = 'articles'
    user = User.objects.get(username=username)
    articles = Article.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    
    context = {'user': user,  'page': page, 'articles': articles, 'profile': profile}
    return render(request,'base/user/Profile.html', context)

def profileLikes(request, username):
    page = 'likes'
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    
    articles = Article.objects.all()
    like_articles = []
    status = False
    
    #Filter for articles
    for article in articles:
        for like in article.likesForArticle.all():
            if like.username == user.username:
                like_articles.append(article)
                if request.user.username == like.username:
                    status = True
        
    context = {'user': user,  'page': page, 'like_articles': like_articles, 'profile': profile, 'status': status}
    return render(request,'base/user/Profile.html', context)

def profileUpdate(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    
    if user:
        if profile:
            if request.method == 'POST':
                email = request.POST.get('email')
                image = request.FILES['image']
                bio = request.POST.get('bio')
                
                twitter = request.POST.get('twitter')
                github = request.POST.get('github')
                telegram = request.POST.get('telegram')
                website = request.POST.get('website')
                
                if image is not None:
                    user.email = email
                
                    profile.image = image
                    profile.bio = bio
                    
                    profile.twitter = twitter
                    profile.github = github
                    profile.telegram = telegram
                    profile.website = website
                
                    user.save()
                    profile.save()
                    return redirect('/profile/'+request.user.username)
                else:
                    messages.error(request, 'Image not found')
        else: 
            messages.add_message(request, 'Profile not found')
    else:
        messages.add_message(request, 'Profile not found')     
    
    context = {'user': user, 'profile': profile}
    return render(request,'base/user/ProfileUpdate.html', context)