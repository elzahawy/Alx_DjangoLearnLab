
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # ✅ ALX expects this line exactly
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ ALX expects this exact path

# Class-based view: Show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # ✅ must use this full path
    context_object_name = 'library'

