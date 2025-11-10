from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from LibraryProject.relationship_app.models import Library, Book   # ✅ ADD THIS LINE



from django.views.generic.detail import DetailView

# Class-based view to show details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

def home(request):
    return render(request, 'relationship_app/list_books.html', {'books': Book.objects.all()})
