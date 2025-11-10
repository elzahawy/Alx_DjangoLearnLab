from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book, Author


# Task 1 Step 3: Enforce Permissions in Views
# Modify views to check for permissions before allowing users to perform certain actions
# Use decorators such as permission_required to enforce these permissions

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books.
    Task 1 Step 3: Protected with can_view permission using @permission_required decorator
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    """View to display a single book - Protected with can_view permission"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'bookshelf/view_book.html', {'book': book})


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    View to add a new book
    Task 1 Step 3: Protected with can_create permission using @permission_required decorator
    Example: Use @permission_required('bookshelf.can_create', raise_exception=True) to protect an add view.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        
        if not title:
            messages.error(request, 'Title is required.')
            authors = Author.objects.all()
            return render(request, 'bookshelf/add_book.html', {'authors': authors})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            authors = Author.objects.all()
            return render(request, 'bookshelf/add_book.html', {'authors': authors})
        
        try:
            author = get_object_or_404(Author, id=author_id)
            book = Book.objects.create(title=title, author=author)
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
        except Exception as e:
            messages.error(request, f'Error creating book: {str(e)}')
            authors = Author.objects.all()
            return render(request, 'bookshelf/add_book.html', {'authors': authors})
    
    authors = Author.objects.all()
    return render(request, 'bookshelf/add_book.html', {'authors': authors})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book
    Task 1 Step 3: Protected with can_edit permission using @permission_required decorator
    Example: Use @permission_required('bookshelf.can_edit', raise_exception=True) to protect an edit view.
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        
        if not title:
            messages.error(request, 'Title is required.')
            authors = Author.objects.all()
            return render(request, 'bookshelf/edit_book.html', {'book': book, 'authors': authors})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            authors = Author.objects.all()
            return render(request, 'bookshelf/edit_book.html', {'book': book, 'authors': authors})
        
        try:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
        except Exception as e:
            messages.error(request, f'Error updating book: {str(e)}')
            authors = Author.objects.all()
            return render(request, 'bookshelf/edit_book.html', {'book': book, 'authors': authors})
    
    authors = Author.objects.all()
    return render(request, 'bookshelf/edit_book.html', {'book': book, 'authors': authors})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book
    Task 1 Step 3: Protected with can_delete permission using @permission_required decorator
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})
