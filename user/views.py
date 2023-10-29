from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.contrib import messages

# Create your views here.

def user_profile(request):
    return render(request, 'user/user_profile.html')


def change_username(request):
    present_user = request.user
    if present_user.is_authenticated:
        if request.method == 'POST':
            present_user.username = request.POST["username"]
            present_user.save()
            return render(request, 'user/user_profile.html')
        return render(request, 'user/user_profile.html')
    else:
        return render(request, 'user/user_profile', {'error': '사용자가 로그인하지 않았습니다.'})