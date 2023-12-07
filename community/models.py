from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import requests


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    hit = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name='like_posts')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='community_thumbnail', null=True)
    content = models.TextField()
    github_address = models.URLField(null=True)
    
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    def md_to_gfm(self):
        headers = {'Content-Type': 'text/plain'}
        data = self.content.encode('utf-8')
        r = requests.post('https://api.github.com/markdown/raw', headers=headers, data=data)

        return r.text
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content