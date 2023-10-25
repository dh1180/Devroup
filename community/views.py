from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms_markdownx import PostForm
from django.conf import settings
import os
from django.contrib import messages

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'community/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.author = request.user.username
        if "image" in request.FILES:
            post.image = request.FILES["image"]
        else:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'community_thumbnail', 'non_image.png')
            with open(default_image_path, 'rb') as default_image_file:
                post.image.save('non_image.png', default_image_file, save=True)
                post.save()
                return redirect('community:post_detail', pk=post.pk)
    return render(request, 'community/post_create.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.hit += 1
    post.save()
    if request.method == 'POST':
        if request.user.is_authenticated:
            post.like += 1
            post.save()
        else:
            messages.warning(request, "로그인 후 다시 시도해 주세요.")
    return render(request, 'community/post_detail.html', {'post': post})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'community/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'community/post_confirm_delete.html', {'post': post})

def change_username(request):
    present_user = request.user
    if present_user.is_authenticated:
        if request.method == 'POST':
            present_user.username = request.POST["username"]
            present_user.save()
            return render(request, 'community/post_list.html')
        return render(request, 'community/user_profile.html')
    else:
        return render(request, 'community/post_list.html', {'error': '사용자가 로그인하지 않았습니다.'})