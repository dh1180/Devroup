from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms_markdownx import PostForm
from django.conf import settings
import os
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Create your views here.
def post_list(request):
    query = request.GET.get('q', '')
    ordering = request.GET.get('ordering', '-date')
    page_number = request.GET.get('page')
    
    if(ordering == ''):
        ordering = '-date'

    if is_ajax(request=request):
        posts = Post.objects.filter(title__icontains=query).order_by(ordering)
        template = loader.get_template('community/post_list_ajax.html')

        paginator = Paginator(posts, 16)
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj}
        html = template.render(context)
        return HttpResponse(html)

    if query:
        posts = Post.objects.filter(title__icontains=query).order_by(ordering)
    else:
        posts = Post.objects.all().order_by(ordering)

    paginator = Paginator(posts, 16)
    page_obj = paginator.get_page(page_number)
    return render(request, 'community/post_list.html', {'page_obj': page_obj})

def post_create(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.author = request.user
        post.github_address = request.POST["github_address"]
        if "image" in request.FILES:
            post.image = request.FILES["image"]
            post.save()
            return redirect('community:post_detail', pk=post.pk)
        else:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'logo', 'Devroup_default_transparent.png')
            with open(default_image_path, 'rb') as default_image_file:
                post.image.save('Devroup_default_transparent.png', default_image_file, save=True)
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
            if post.like_users.filter(pk=request.user.pk).exists():
                post.like_users.remove(request.user)
                post.like -= 1
            else:
                post.like_users.add(request.user)
                post.like += 1
            post.save()
        else:
            messages.warning(request, "로그인 후 다시 시도해 주세요.")
    return render(request, 'community/post_detail.html', {'post': post, 'comments': comments})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.author = request.user
        post.github_address = request.POST["github_address"]
        if "image" in request.FILES:
            post.image = request.FILES["image"]
            post.save()
            return redirect('community:post_detail', pk=post.pk)
        else:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'community_thumbnail', 'non_image.png')
            with open(default_image_path, 'rb') as default_image_file:
                post.image.save('non_image.png', default_image_file, save=True)
                post.save()
                return redirect('community:post_detail', pk=post.pk)
    return render(request, 'community/post_edit.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('community:post_list')
    return render(request, 'community/post_detail.html', {'post': post})

