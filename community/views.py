from django.shortcuts import render
from . import models
from .forms_markdownx import PostForm

# Create your views here.

def index(request):
    return render(request, 'community/index.html')

def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'community/main.html', {'form': form})