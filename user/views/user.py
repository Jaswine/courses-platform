from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Profile


def settings(request):
    
    
    context = {
        
    }
    return render(request, 'auth/settings.html', context)
