from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.contrib import messages
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from community.models import Post

# Create your views here.

def user_profile(request):
    return render(request, 'user/user_profile.html')


def user_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-date')
    return render(request, 'user/user_posts.html', {'posts': posts})


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