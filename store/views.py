from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer, CategoryCreareOrReadSerializer, CommentaryCreatOrReadSerializer, BookListSerializer
from .models import Book, Category, Commentary

# Create your views here.

class BookListView(APIView):
    def get(self, request, fomrat=None):
        books = Book.objects.all().prefetch_related('author', 'categories')
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, fomrat=None):
        data = request.data.copy()
        serializer = BookListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookDetailView(APIView):
    def get(self, request, pk=None, format=None):
        book = get_object_or_404(Book.objects.all().prefetch_related('author', 'categories', 'commentary', 'commentary__author'), pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None, fomrat=None):
        data = request.data.copy()
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentaryListView(APIView):
    def get(self, request, book_pk=None, format=None):
        commentary_on_the_book = Commentary.objects.filter(book_id=book_pk).prefetch_related('author')
        serializer = CommentaryCreatOrReadSerializer(commentary_on_the_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, book_pk, format=None):
        data = request.data.copy()
        data['book_id'] = book_pk
        serializer = CommentaryCreatOrReadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CommentaryDetailView(APIView):
    def get(self, request, pk, format=None):
        comment = get_object_or_404(Commentary.objects.select_related('author'), pk=pk)
        serializer = CommentaryCreatOrReadSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, book_pk, comment_pk, format=None):
        data = request.data.copy()
        comment = get_object_or_404(Commentary.objects.all().prefetch_related('author'), pk=comment_pk)
        serializer = CommentaryCreatOrReadSerializer(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, book_pk, comment_pk, format=None):
        comment = get_object_or_404(Commentary, pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CategoryListView(APIView):
    def get(self, request, fomrat=None):
        categories = Category.objects.all().prefetch_related('books', 'books__author')
        serializer = CategoryCreareOrReadSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request , format=None):
        data = request.data.copy()
        serializer = CategoryCreareOrReadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class BooksByCategory(APIView):
    def get(self, request, pk=None, format=None):
        books_by_category = get_object_or_404(Category.objects.prefetch_related('books', 'books__author'), pk=pk)
        serializer = CategoryCreareOrReadSerializer(books_by_category)
        return Response(serializer.data, status=status.HTTP_200_OK)