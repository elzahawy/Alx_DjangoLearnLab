from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


# BookSerializer handles individual book objects.
# It includes custom validation for publication_year.
class BookSerializer(serializers.ModelSerializer):

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


# AuthorSerializer serializes author data AND includes nested books.
class AuthorSerializer(serializers.ModelSerializer):
    # "books" refers to related_name='books' in the Book model
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']


# api/serializers.py
from rest_framework import serializers
from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())  # Accept ID

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']  # include all required fields

