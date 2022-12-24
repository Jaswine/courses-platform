from django.shortcuts import render
from .models import  *

def home(request):
    context = {}
    return render(request, 'base/Home.html', context)

#! _______________________AUTH_____________________
def registration(request):
    context = {}
    return render(request,'base/Registration.html', context)

def login(request):
    context = {}
    return render(request,'base/Login.html', context)