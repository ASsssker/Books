from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookCreateOrReadSerializer, BookUpdateSerializer, CategoryCreareOrReadSerializer, CommentaryCreatOrReadSerializer
from .models import Book, Category, Commentary

# Create your views here.

class BookListView(APIView):
    def get(self, request, fomrat=None):
        books = Book.objects.all().prefetch_related('author', 'categories')
        serializer = BookCreateOrReadSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, fomrat=None):
        data = request.data.copy()
        serializer = BookCreateOrReadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookDetailView(APIView):
    def get(self, request, pk=None, format=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookCreateOrReadSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None, fomrat=None):
        data = request.data.copy()
        book = get_object_or_404(Book, pk=pk)
        serializer = BookUpdateSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CommentaryListView(APIView):
    def get(self, request, book_pk=None, format=None):
        commentary_on_the_book = Commentary.objects.filter(book_id=book_pk)
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
    

class CategoryListView(APIView):
    def get(self, request, fomrat=None):
        categories = Category.objects.all()
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
        books_by_category = get_object_or_404(Category.objects.prefetch_related('books'), pk=pk)
        serializer = CategoryCreareOrReadSerializer(books_by_category)
        return Response(serializer.data, status=status.HTTP_200_OK)