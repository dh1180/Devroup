from django.db import models
from markdownx.models import MarkdownxField


"""
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ChatField(max_length=30)
    description = models.TextField()
    

    def __str__(self):
        return self.title
"""

class MyModel(models.Model):
    myfield = MarkdownxField()
    