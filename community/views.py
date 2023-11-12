from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms_markdownx import PostForm
from django.conf import settings
import os
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template import loader

# Create your views here.
def post_list(request):
    query = request.GET.get('q', '')
    ordering = request.GET.get('ordering', '-date')
    
    if request.is_ajax():
        posts = Post.objects.filter(title__icontains=query).order_by(ordering)
        template = loader.get_template('community/post_list.html')  # 게시물을 렌더링할 HTML 템플릿
        context = {'posts': posts}
        html = template.render(context)
        return HttpResponse(html)

    if query:
        posts = Post.objects.filter(title__icontains=query).order_by(ordering)
    else:
        posts = Post.objects.all().order_by(ordering)
        
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
    comments = Comment.objects.filter(post__pk=pk).order_by('-date')
    if request.method == 'POST':
        if request.user.is_authenticated:
            post.like += 1
            post.save()
        else:
            messages.warning(request, "로그인 후 다시 시도해 주세요.")
    return render(request, 'community/post_detail.html', {'post': post, 'comments': comments})

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
