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
