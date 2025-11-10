from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .models import Library
from .models import Author
from .models import CustomUser


def list_books(request):
    """
    Function-based view that lists all books with their authors.
    This view should render a simple text list of book titles and their authors.
    Task 1: Protected with can_view permission
    """
    # Task 1: Check for can_view permission
    if not request.user.has_perm('relationship_app.can_view'):
        messages.error(request, 'You do not have permission to view books.')
        return redirect('login')
    
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


def list_libraries(request):
    """Function-based view that lists all libraries."""
    libraries = Library.objects.all()
    return render(request, 'relationship_app/list_libraries.html', {'libraries': libraries})


class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library,
    listing all books available in that library.
    Utilizes Django's DetailView.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Authentication Views
def register(request):
    """User registration view - Updated to use CustomUser"""
    if request.method == 'POST':
        from django.contrib.auth.forms import UserCreationForm
        # Note: In production, create a custom form for CustomUser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('list_books')
    else:
        from django.contrib.auth.forms import UserCreationForm
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Role-Based Access Control Views
def is_admin(user):
    """Check if user has Admin role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'

def is_librarian(user):
    """Check if user has Librarian role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'

def is_member(user):
    """Check if user has Member role"""
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    """Admin-only view"""
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    """Librarian-only view"""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    """Member-only view"""
    return render(request, 'relationship_app/member_view.html')


# Task 1: Permission-Based Views for Books
# Using the custom permissions: can_view, can_create, can_edit, can_delete

@permission_required('relationship_app.can_view', raise_exception=True)
def view_book(request, book_id):
    """View to display a single book - Task 1: Protected with can_view permission"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'relationship_app/view_book.html', {'book': book})

@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """
    View to add a new book
    Task 1: Protected with can_create permission (using can_create instead of can_add_book)
    Task 2: Secure data access - using Django ORM properly, validating input
    """
    if request.method == 'POST':
        # Task 2: Secure data access - validate and sanitize input
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        
        # Validate input
        if not title:
            messages.error(request, 'Title is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
        
        # Task 2: Use Django ORM properly - parameterized query (get_object_or_404)
        try:
            author = get_object_or_404(Author, id=author_id)
            # Task 2: Use ORM create method instead of raw SQL
            book = Book.objects.create(title=title, author=author)
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('list_books')
        except Exception as e:
            messages.error(request, f'Error creating book: {str(e)}')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
    
    # Task 2: Use ORM query properly
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book
    Task 1: Protected with can_edit permission
    Task 2: Secure data access - using Django ORM properly, validating input
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Task 2: Secure data access - validate and sanitize input
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        
        # Validate input
        if not title:
            messages.error(request, 'Title is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})
        
        # Task 2: Use Django ORM properly - parameterized query
        try:
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('list_books')
        except Exception as e:
            messages.error(request, f'Error updating book: {str(e)}')
            authors = Author.objects.all()
            return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})

@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book
    Task 1: Protected with can_delete permission
    Task 2: Secure data access - using Django ORM properly
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # Task 2: Use ORM delete method instead of raw SQL
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})


# Task 2: Secure search functionality
@login_required
def search_books(request):
    """
    Secure search view - Task 2: Prevents SQL injection by using Django ORM
    """
    query = request.GET.get('q', '').strip()
    books = []
    
    if query:
        # Task 2: Use Django ORM filter with Q objects - prevents SQL injection
        # Never use string formatting or raw SQL for user input
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    
    return render(request, 'relationship_app/search_books.html', {'books': books, 'query': query})

