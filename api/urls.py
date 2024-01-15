from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('book/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:book_pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:book_pk>/commentary/', views.CommentaryListView.as_view(), name='commentary_list'),
    path('book/<int:book_pk>/commentary/<int:comment_pk>/', views.CommentaryDetailView.as_view(), name='commentary_detail'),
]
