from django.db import models

# Author model stores writer information.
# One Author -> Many Books.
class Author(models.Model):
    name = models.CharField(max_length=255)  # Author's full name

    def __str__(self):
        return self.name


# Book model belongs to an Author through a ForeignKey.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',   # allows nested serialization: author.books
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

# Create your models here.
