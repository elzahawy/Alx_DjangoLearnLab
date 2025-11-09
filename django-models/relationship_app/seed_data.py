import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from relationship_app.query_samples import books_by_author, books_in_library, librarian_for_library

# Clear old data
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create authors
a1 = Author.objects.create(name="J.K. Rowling")
a2 = Author.objects.create(name="George Orwell")

# Create books
b1 = Book.objects.create(title="Harry Potter 1", author=a1)
b2 = Book.objects.create(title="Harry Potter 2", author=a1)
b3 = Book.objects.create(title="1984", author=a2)

# Create library
lib = Library.objects.create(name="Central Library")
lib.books.add(b1, b2, b3)

# Create librarian
Librarian.objects.create(name="Alice", library=lib)

# Test queries
print([b.title for b in books_by_author("J.K. Rowling")])
print([b.title for b in books_in_library("Central Library")])
print(librarian_for_library("Central Library").name)
