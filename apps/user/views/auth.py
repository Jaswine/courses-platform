from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from ..forms import CreateUserForm
from ..utils.auth_util import authenticate


def sign_in(request):
    """
        Вход пользователя в аккаунт
    """
    pass
    # if request.user.is_authenticated:
    #     return redirect('/')
    #
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     user = authenticate(email, password=password)
    #
    #     if user:
    #         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    #         messages.success(request, f'Welcome {user.username}!')
    #         return redirect('/')
    #     messages.error(request, 'Invalid username or password')
    #
    # return render(request, 'auth/auth.html', {'type': 'Sign In'})


def sign_up(request):
    """
        Регистрация пользователя в аккаунт
    """
    pass
    # if request.user.is_authenticated:
    #     return redirect('/')
    #
    # form = CreateUserForm()
    #
    # if request.method == 'POST':
    #     form = CreateUserForm(request.POST)
    #     user = create_user_and_profile_by_form(form)
    #
    #     if user:
    #         login(request,
    #               user,
    #               backend='django.contrib.auth.backends.ModelBackend')
    #         return redirect('/')
    #
    # return render(request, 'auth/auth.html', {
    #     'type': 'Sign Up',
    #     'form': form,
    # })


@login_required(login_url='auth:sign-in')
def sign_out(request):
    """
        Выход пользователя из аккаунта
    """
    logout(request)
    messages.success(request, 'You have been signed out successfully!')
    return redirect('/sign-in')
