from django.test import TestCase
from django.urls import reverse
from django.forms.models import model_to_dict
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, User, Category
from .serializers import BookSerializer

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_request_list_view(self):
        url = reverse('book_list')
        data = {'title': 'test title 2', 'description': 'test description 2',
                'publication_date': '2023-12-22'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        
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
        
        
    
