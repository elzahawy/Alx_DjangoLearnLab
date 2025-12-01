from django.shortcuts import render

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    # For now, just render a simple template or reuse base.html
    return render(request, 'blog/base.html')  # you can change this later
# Create your views here.
