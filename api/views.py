from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookReadSerializer, CommentaryCreatOrReadSerializer, CommentaryUpdateSerializer
from store.models import Book, Commentary

# Create your views here.

class BookListView(APIView):
    def get(self, request, fomrat=None):
        books = Book.objects.prefetch_related('author', 'categories')
        serializer = BookReadSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BookDetailView(APIView):
    def get(self, request, book_pk, format=None):
        book = get_object_or_404(Book.objects.prefetch_related('author', 'categories'), pk=book_pk)
        serializer = BookReadSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentaryListView(APIView):
    def get(self, request, book_pk, format=None):
        commentary_on_the_book = Commentary.objects.filter(book_id=book_pk).select_related('author')
        serializer = CommentaryCreatOrReadSerializer(commentary_on_the_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, book_pk, format=None):
        data = request.data.copy()
        author = {'id': request.user.id, 'username': request.user.username}
        data['book_id'] = book_pk
        data['author'] = author
        print(data)
        serializer = CommentaryCreatOrReadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentaryDetailView(APIView):
    def get(self, request, book_pk, comment_pk, format=None):
        comment = get_object_or_404(Commentary.objects.filter(book_id=book_pk).select_related('author'), pk=comment_pk)
        serializer = CommentaryCreatOrReadSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, book_pk, comment_pk, format=None):
        data = request.data.copy()
        comment = get_object_or_404(Commentary, pk=comment_pk)
        serializer = CommentaryUpdateSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_pk, comment_pk, format=None):
        comment = Commentary.objects.filter(pk=comment_pk).delete()
        return Response(status=status.HTTP_200_OK)