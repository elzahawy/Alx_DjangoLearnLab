from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from LibraryProject.bookshelf.models import Book, Author, CustomUser
from .models import Library


def list_books(request):
    """
    Function-based view that lists all books with their authors.
    This view should render a simple text list of book titles and their authors.
    Task 1: Protected with can_view permission
    """
    # Task 1: Check for can_view permission
    if not request.user.has_perm('bookshelf.can_view'):
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

@permission_required('bookshelf.can_view', raise_exception=True)
def view_book(request, book_id):
    """View to display a single book - Task 1: Protected with can_view permission"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'relationship_app/view_book.html', {'book': book})

# Task 1 Step 3: Enforce Permissions in Views
# This view is protected with the can_create permission
# Using @permission_required decorator to check permissions before allowing access
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    View to add a new book
    
    Task 1 Step 3: Protected with can_create permission using @permission_required decorator
    Task 2 Step 3: Secure data access - using Django ORM properly, validating input to prevent SQL injection
    
    Security measures:
    - Permission check: Only users with can_create permission can access
    - Input validation: Validates title and author_id are provided
    - Input sanitization: Strips whitespace from title
    - ORM usage: Uses Django ORM (get_object_or_404, objects.create) instead of raw SQL
    - Error handling: Try-except block for safe error handling
    """
    if request.method == 'POST':
        # Task 2 Step 3: Secure data access - validate and sanitize user input
        # Strip whitespace to sanitize input and prevent issues
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        
        # Task 2 Step 3: Validate input to ensure required fields are present
        # This prevents invalid data from being processed
        if not title:
            messages.error(request, 'Title is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
        
        # Task 2 Step 3: Use Django ORM properly - parameterized query (get_object_or_404)
        # This prevents SQL injection by using Django's ORM instead of raw SQL
        # get_object_or_404 safely retrieves objects and handles not found cases
        try:
            author = get_object_or_404(Author, id=author_id)
            # Task 2 Step 3: Use ORM create method instead of raw SQL
            # Book.objects.create() uses parameterized queries internally, preventing SQL injection
            book = Book.objects.create(title=title, author=author)
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('list_books')
        except Exception as e:
            # Task 2 Step 3: Error handling - catch exceptions safely
            messages.error(request, f'Error creating book: {str(e)}')
            authors = Author.objects.all()
            return render(request, 'relationship_app/add_book.html', {'authors': authors})
    
    # Task 2 Step 3: Use ORM query properly - no raw SQL
    # Author.objects.all() uses Django ORM, which is safe from SQL injection
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

@permission_required('bookshelf.can_edit', raise_exception=True)
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

@permission_required('bookshelf.can_delete', raise_exception=True)
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


# Task 2 Step 3: Secure Data Access in Views
# Secure search functionality - prevents SQL injection by using Django ORM
@login_required
def search_books(request):
    """
    Secure search view
    
    Task 2 Step 3: Prevents SQL injection by using Django ORM instead of raw SQL
    
    Security measures:
    - Input sanitization: Strips whitespace from query
    - ORM usage: Uses Django ORM Q objects for filtering
    - No raw SQL: Never uses string formatting or raw SQL queries
    - Parameterized queries: Django ORM automatically parameterizes queries
    
    Example of what NOT to do (SQL injection vulnerable):
    # NEVER: Book.objects.raw(f"SELECT * FROM books WHERE title = '{query}'")
    # NEVER: Book.objects.extra(where=[f"title LIKE '%{query}%'"])
    """
    # Task 2 Step 3: Sanitize user input - strip whitespace
    query = request.GET.get('q', '').strip()
    books = []
    
    if query:
        # Task 2 Step 3: Use Django ORM filter with Q objects - prevents SQL injection
        # Q objects allow complex queries while maintaining security
        # Django ORM automatically parameterizes these queries, preventing SQL injection
        # Never use string formatting or raw SQL for user input
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        )
    
    return render(request, 'relationship_app/search_books.html', {'books': books, 'query': query})

