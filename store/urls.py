from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    CategoryListView,
    BooksByCategory
)


urlpatterns = [
    path('book/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', BooksByCategory.as_view(), name='books_by_category'),
]
