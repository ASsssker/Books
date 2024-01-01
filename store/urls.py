from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    CategoryListView,
    BooksByCategory,
    CommentaryListView,
)


urlpatterns = [
    path('book/', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/<int:book_pk>/commentary/', CommentaryListView.as_view(), name='commentary_on_the_book'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/book/', BooksByCategory.as_view(), name='books_by_category'),
]
