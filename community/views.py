from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms_markdownx import PostForm
from django.conf import settings
import os

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST["title"]
        post.content = request.POST["content"]
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