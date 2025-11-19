from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    return render(request, "bookshelf/view_books.html")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return render(request, "bookshelf/create_book.html")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return render(request, "bookshelf/edit_book.html")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, "bookshelf/delete_book.html")

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return render(request, "bookshelf/book_list.html")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return render(request, "bookshelf/create_book.html")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return render(request, "bookshelf/edit_book.html")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, "bookshelf/delete_book.html")

from django.shortcuts import render, redirect
from .forms import ExampleForm
from .models import Book

# Example form view
def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Safe handling of form data
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

# Book list view
def book_list_view(request):
    books = Book.objects.all()  # Safe ORM query
    return render(request, 'bookshelf/book_list.html', {'books': books})
