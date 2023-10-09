from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=30, null=True)
    hit = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    content = MarkdownxField()
    
    def md(self):
        return markdown(self.content)
    
    def __str__(self):
        return self.title