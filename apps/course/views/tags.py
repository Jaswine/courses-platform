from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='auth:sign-in')
def tags(request):
    return render(request, 'course/tags.html')
    