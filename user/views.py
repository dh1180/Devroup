from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.contrib import messages
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from community.models import Post, Comment
from django.contrib.auth.models import User

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
    

def user_comment_posts(request):
    comment_posts = Comment.objects.filter(author=request.user).order_by('-date')
    return render(request, 'user/user_comment_posts.html', {'comment_posts': comment_posts})


def user_like_posts(request):
    posts = Post.objects.filter(like_users=request.user).order_by('-date')
    return render(request, 'user/user_like_posts.html', {'posts': posts})
    
    
def user_delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('community:post_list')
    return render(request, 'user/user_profile')

def other_user_posts(request, author):
    posts = Post.objects.filter(author=author).order_by('-date')
    return render(request, 'user/other_user_posts.html', {'posts': posts, 'author': User.objects.get(pk=author)})