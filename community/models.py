from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import requests


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=30, null=True)
    hit = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='community_thumbnail', null=True)
    content = models.TextField()
    
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=30, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content