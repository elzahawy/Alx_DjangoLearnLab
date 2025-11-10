from django.urls import path
from .views import list_books, list_libraries, LibraryDetailView, register_view, login_view, logout_view

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/', list_libraries, name='list_libraries'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]