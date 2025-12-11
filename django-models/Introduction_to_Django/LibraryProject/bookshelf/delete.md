# Delete the Book

```python
from bookshelf.models import Book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()
Book.objects.all()
```

# Expected Output:
# <QuerySet []>  # confirms the book was deleted

