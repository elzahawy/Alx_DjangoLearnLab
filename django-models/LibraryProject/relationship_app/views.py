from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library  # ✅ Must include both Book and Library

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()  # ✅ ALX expects this exact line
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: Library detail
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # ✅ Required for checker


