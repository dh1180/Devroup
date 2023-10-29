from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.conf import settings
import os
from django.contrib import messages

# Create your views here.


def comment_create(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        comment = Comment()
        comment.post = post
        comment.author = request.user.username
        comment.content = request.POST["content"]
        comment.save()
        return redirect('community:post_detail', pk=post.pk)
    messages.warning(request, "로그인 후 다시 시도해 주세요.")


def comment_delete(request, post_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user.username == comment.author:
            comment.delete()
    return redirect('community:post_detail', pk=post_pk)