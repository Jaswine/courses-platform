from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.forms import AuthenticationForm
from ..forms import CreateUserForm

from django.contrib.auth.models import User
from ..models import Profile


def registration_view(request):
   
   if request.user.is_authenticated:
      return redirect('base:profile', request.user.username)
   
   page_type = 'registration'
   
   form = CreateUserForm()
   
   if request.method == 'POST':
      # get data from form
      form = CreateUserForm(request.POST)
      
      # check if form is valid
      if form.is_valid():
         new_user = form.save(commit=False)
         new_user.save()
                  
         # login user
         login(request, new_user, backend='django.contrib.auth.backends.ModelBackend' )
         return redirect('base:index')
         
   context = {
      'page_type': page_type, 
      'form': form
   }
   return render(request, 'base/auth.html', context)

# login
def login_view(request):
   page_type = 'login'
   
   if request.user.is_authenticated:
      return redirect('base:profile', request.user.username)
   
   if request.method == 'POST':
      # get data from form
      name = request.POST.get('username')
      password = request.POST.get('password')
            
      try:
         user = User.objects.get(username=name)
      except:
         messages.error(request, 'User not found')
      
      user = authenticate(username=name, password=password)

      
      if user is not None:
         login(request, user)
         return redirect('base:index')
      else:
         messages.error(request, 'Invalid password or username')
   
   context = {
      'page_type': page_type,
   }
   return render(request, 'base/auth.html', context)

# logout
def logout_view(request):
   logout(request)
   return redirect('base:index') 