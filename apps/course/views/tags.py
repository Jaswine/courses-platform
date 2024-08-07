from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.models import User
from ..models import Tag


@login_required(login_url='auth:sign-in')
def tags(request):
    return render(request, 'course/tags.html')
    