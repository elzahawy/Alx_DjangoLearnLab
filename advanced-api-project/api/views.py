"""
This module contains the Book CRUD API endpoints using Django REST Framework's
generic views. Each view handles a specific CRUD action and applies appropriate
permissions.

Views included:
- BookListView: List all books (public)
- BookDetailView: Retrieve a specific book (public)
- BookCreateView: Create a book (authenticated users only)
- BookUpdateView: Update a book (authenticated users only)
- BookDeleteView: Delete a book (authenticated users only)
"""

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer


# -------------------------------
# LIST VIEW — Anyone can view books
# -------------------------------
class BookListView(generics.ListAPIView):
    """
    Retrieves a list of all books.
    Read-only — no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------
# DETAIL VIEW — Anyone can view a single book
# -------------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID.
    Read-only — no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# -------------------------------
# CREATE VIEW — Only authenticated users can add books
# -------------------------------
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book entry.
    Requires authentication.
    Includes built-in serializer validation.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# UPDATE VIEW — Only authenticated users can modify books
# -------------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Requires authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# -------------------------------
# DELETE VIEW — Only authenticated users can delete
# -------------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book entry.
    Requires authentication.
    """
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

# Create your views here.
