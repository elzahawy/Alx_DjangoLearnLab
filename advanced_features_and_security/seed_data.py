import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

# now import your models
from relationship_app.models import Author, Book, Library, Librarian

# Example seed logic:
def run():
    # create authors
    author1 = Author.objects.create(name="J.R.R. Tolkien")
    author2 = Author.objects.create(name="George R.R. Martin")

    # create books
    book1 = Book.objects.create(title="The Hobbit", author=author1)
    book2 = Book.objects.create(title="Game of Thrones", author=author2)

    # create library
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2)

    # create librarian
    Librarian.objects.create(name="John Doe", library=library)

if __name__ == "__main__":
    run()
