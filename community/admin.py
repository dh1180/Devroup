from django.contrib import admin
from .models import Post, Comment
from django.db import models


admin.site.register(Post)
admin.site.register(Comment)