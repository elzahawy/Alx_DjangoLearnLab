from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    # POST same as list
    path('books/', BookCreateView.as_view()),

    # PUT & DELETE same as detail
    path('books/<int:pk>/', BookUpdateView.as_view()),
    path('books/<int:pk>/', BookDeleteView.as_view()),
]
