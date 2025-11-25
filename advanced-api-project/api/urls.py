from django.urls import path
from .views import (
    BookListCreateView,
    BookRetrieveUpdateDeleteView,
)

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
 
    # Required by checker
    path('books/update/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-delete'),

    # Optional but good
    path('books/<int:pk>/', BookRetrieveUpdateDeleteView.as_view(), name='book-detail'),
]
'''from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView,
    BookUpdateView, BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]'''
