from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..forms import CreateUserForm
from ..utils import authenticate


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email, password=password)
        
        if user:
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome {user.username}!')
            return redirect('/')
        else:
             messages.error(request, 'Invalid username or password')
                
    return render(request, 'auth/auth.html', {'type': 'Sign In'})

def sign_up(request):    
    if request.user.is_authenticated:
        return redirect('/')
    
    form = CreateUserForm()
    
    if request.method == 'POST':
      form = CreateUserForm(request.POST)
      
      if form.is_valid():
         new_user = form.save(commit=False)
         new_user.save()
                  
         login(request, new_user, backend='django.contrib.auth.backends.ModelBackend' )
         return redirect('/')
     
    return render(request, 'auth/auth.html', {
        'type': 'Sign Up',
        'form': form,
    })

@login_required(login_url='auth:sign-in')
def sign_out(request):
    logout(request)
    messages.success(request, 'You have been signed out successfully!')
    return redirect('/sign-in')