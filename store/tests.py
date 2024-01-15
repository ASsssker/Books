from django.test import TestCase
from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, User, Category
from .serializers import BookSerializer, BookListSerializer, CategoryCreareOrReadSerializer

# Create your tests here.


class BookTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(email='test@test.com', password='12345')
        user.username = 'test_user'
        user.is_superuser = True
        self.client.login(username=user.email, password='12345')
        self.book = Book(
            title='test title 1',
            description='test description 1',
            publication_date='2022-12-22'
        )
        self.book.save()
        
    def test_get_request_list_view(self):
        url = reverse('book_list')
        response = self.client.get(url)
        books = BookListSerializer(Book.objects.all().prefetch_related('author', 'categories'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, books.data)
    
    def test_post_request_list_view(self):
        url = reverse('book_list')
        data = {'title': 'test title 2', 'description': 'test description 2',
                'publication_date': '2023-12-22'}
        response = self.client.post(url, data)
        book_data = BookListSerializer(Book.objects.filter(**data).first())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data, book_data.data)
        
    def test_get_detail_view(self):
        id=1
        url = reverse('book_detail', args=[id])
        response = self.client.get(url)
        book = BookSerializer(Book.objects.get(id=id))
        self.assertEqual(response.data, book.data)
        
    def test_put_detail_view(self):
        id = 1
        url = reverse('book_detail', args=[id])
        data = {'title': 'updated title', 'description': 'updated description',
                'publication_date': '2010-12-22'}
        response = self.client.put(url, data)
        book = BookSerializer(Book.objects.get(id=id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book.data)
        
    def test_delete_detail_view(self):
        id = 1
        url = reverse('book_detail', args=[id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    
class CategoryTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(email='test@test.com', password='12345')
        user.username = 'test_user'
        user.is_superuser = True
        self.client.login(username=user.email, password='12345')
        book = Book(
            title='test title 1',
            description='test description 1',
            publication_date='2022-12-22'
        )
        book.save()
        self.category_1 = Category.objects.create(name='test category 1')
        self.category_1.books.add(book)
        self.category_2 = Category.objects.create(name='test category 2')
        self.category_2.books.add(book)
        
    def test_get_request_category_view(self):
        url = reverse('category_list')
        response = self.client.get(url)
        book_categories = CategoryCreareOrReadSerializer(Category.objects.all().prefetch_related('books', 'books__author'), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book_categories.data)    
            
    def test_post_request_category_view(self):
        url = reverse('book_list')
        data = {'name': 'test category 3'}
        response = self.client.post(url, data)
        book_categories = CategoryCreareOrReadSerializer(Category.objects.filter(**data).first())
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, book_categories.data)