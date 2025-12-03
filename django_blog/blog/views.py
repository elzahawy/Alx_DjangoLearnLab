from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/base.html', {'posts': posts})

# Create your views here.
