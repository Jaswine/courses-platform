from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from ..forms import UpdateUserForm
from ..services.user_service import get_user_by_username

#
# @login_required(login_url='auth:sign-in')
# def settings(request):
#     """
#         Обновление пользователя
#     """
#     profile = get_object_or_404(User, user=request.user)
#
#     formUser = UpdateUserForm(instance=request.user)
#     formProfile = UpdateProfileForm(instance=profile)
#
#     if request.method == 'POST':
#         formUser = UpdateUserForm(request.POST, instance=request.user)
#         formProfile = UpdateProfileForm(request.POST, request.FILES, instance=profile)
#
#         if update_user_and_profile_by_forms(formUser, formProfile):
#             messages.success(request, 'Your profile has been updated successfully!')
#             return redirect('auth:dashboard')
#         messages.error(request, 'Something went wrong. Please try again.')
#         return redirect('auth:settings')
#
#     return render(request, 'auth/settings.html', {
#         'formUser': formUser,
#         'formProfile': formProfile,
#     })
#
#
# def profile(request, username):
#     """
#         Профиль пользователя
#     """
#     user = get_object_or_404(User, username=username)
#     profile = get_object_or_404(Profile, user=user)
#
#     return render(request, 'auth/profile.html', {
#         'status': 'profile',
#         'user': user,
#         'profile': profile,
#     })
#
#
# def certificates(request, username):
#     """
#         Сертификаты пользователя
#     """
#     user = User.objects.get(username=username)
#     profile = Profile.objects.get(user=user)
#
#     return render(request, 'auth/profile.html', {
#         'status': 'certificates',
#         'user': user,
#         'profile': profile,
#     })
