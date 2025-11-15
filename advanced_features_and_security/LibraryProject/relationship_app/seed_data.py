import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from LibraryProject.relationship_app.models import Author, Book, Library, Librarian

# Clear existing data (optional, useful for reruns)
Librarian.objects.all().delete()
Library.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()

# Create Authors
authors = [
    Author.objects.create(name="J.K. Rowling"),
    Author.objects.create(name="J.R.R. Tolkien"),
    Author.objects.create(name="George Orwell"),
    Author.objects.create(name="Jane Austen"),
    Author.objects.create(name="Charles Dickens"),
    Author.objects.create(name="Mark Twain"),
    Author.objects.create(name="Ernest Hemingway"),
    Author.objects.create(name="F. Scott Fitzgerald"),
    Author.objects.create(name="Virginia Woolf"),
    Author.objects.create(name="Agatha Christie"),
]

# Create Books (at least 5 books per library, creating enough for multiple libraries)
books = [
    # J.K. Rowling books
    Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=authors[0]),
    Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=authors[0]),
    Book.objects.create(title="Harry Potter and the Prisoner of Azkaban", author=authors[0]),
    # J.R.R. Tolkien books
    Book.objects.create(title="The Hobbit", author=authors[1]),
    Book.objects.create(title="The Fellowship of the Ring", author=authors[1]),
    Book.objects.create(title="The Two Towers", author=authors[1]),
    Book.objects.create(title="The Return of the King", author=authors[1]),
    # George Orwell books
    Book.objects.create(title="1984", author=authors[2]),
    Book.objects.create(title="Animal Farm", author=authors[2]),
    # Jane Austen books
    Book.objects.create(title="Pride and Prejudice", author=authors[3]),
    Book.objects.create(title="Sense and Sensibility", author=authors[3]),
    Book.objects.create(title="Emma", author=authors[3]),
    # Charles Dickens books
    Book.objects.create(title="A Tale of Two Cities", author=authors[4]),
    Book.objects.create(title="Great Expectations", author=authors[4]),
    Book.objects.create(title="Oliver Twist", author=authors[4]),
    # Mark Twain books
    Book.objects.create(title="The Adventures of Tom Sawyer", author=authors[5]),
    Book.objects.create(title="Adventures of Huckleberry Finn", author=authors[5]),
    # Ernest Hemingway books
    Book.objects.create(title="The Old Man and the Sea", author=authors[6]),
    Book.objects.create(title="A Farewell to Arms", author=authors[6]),
    # F. Scott Fitzgerald books
    Book.objects.create(title="The Great Gatsby", author=authors[7]),
    # Virginia Woolf books
    Book.objects.create(title="Mrs. Dalloway", author=authors[8]),
    # Agatha Christie books
    Book.objects.create(title="Murder on the Orient Express", author=authors[9]),
    Book.objects.create(title="And Then There Were None", author=authors[9]),
]

# Create Libraries
libraries = [
    Library.objects.create(name="Central Library"),
    Library.objects.create(name="Community Library"),
    Library.objects.create(name="University Library"),
    Library.objects.create(name="City Public Library"),
]

# Add 5 books to each library
# Central Library - books 0-4
libraries[0].books.add(books[0], books[1], books[2], books[3], books[4])

# Community Library - books 5-9
libraries[1].books.add(books[5], books[6], books[7], books[8], books[9])

# University Library - books 10-14
libraries[2].books.add(books[10], books[11], books[12], books[13], books[14])

# City Public Library - books 15-19
libraries[3].books.add(books[15], books[16], books[17], books[18], books[19])

# Create Librarians for each library
librarians = [
    Librarian.objects.create(name="Alice Johnson", library=libraries[0]),
    Librarian.objects.create(name="Bob Smith", library=libraries[1]),
    Librarian.objects.create(name="Carol Williams", library=libraries[2]),
    Librarian.objects.create(name="David Brown", library=libraries[3]),
]

print("Seed data created successfully!")
print(f"Created {len(authors)} authors")
print(f"Created {len(books)} books")
print(f"Created {len(libraries)} libraries")
print(f"Created {len(librarians)} librarians")
print("\nLibrary details:")
for library in libraries:
    book_count = library.books.count()
    print(f"  - {library.name}: {book_count} books (Librarian: {library.librarian.name})")

