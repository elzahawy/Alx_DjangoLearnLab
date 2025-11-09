import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data (optional, useful for reruns)
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create Authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="J.R.R. Tolkien")
author3 = Author.objects.create(name="George Orwell")

# Create Books
book1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author1)
book2 = Book.objects.create(title="The Hobbit", author=author2)
book3 = Book.objects.create(title="1984", author=author3)

# Create Libraries
library1 = Library.objects.create(name="Central Library")
library2 = Library.objects.create(name="Community Library")

# Add books to libraries
library1.books.add(book1, book2)
library2.books.add(book3)

# Create Librarians
librarian1 = Librarian.objects.create(name="Alice", library=library1)
librarian2 = Librarian.objects.create(name="Bob", library=library2)

print("Seed data created successfully!")

