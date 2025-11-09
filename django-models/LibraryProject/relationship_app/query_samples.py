# LibraryProject/relationship_app/query_samples.py
from .models import Author, Book, Library, Librarian

def books_by_author(author_name):
    # Get the author object
    author = Author.objects.get(name=author_name)
    # Return all books by this author
    return Book.objects.filter(author=author)

def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

