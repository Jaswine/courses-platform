from django.shortcuts import render, redirect
from .models import  Tag
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator, CommonPasswordValidator, NumericPasswordValidator


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