from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self) -> str:
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        
    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    author = models.ManyToManyField(Author, related_name='books')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    file = models.FileField(upload_to='books/%Y/%m/%d/', null=True, blank=True)
    publication_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='books')
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['title']
        indexes = [
            models.Index(fields=['title', 'description']),
            models.Index(fields=['created'])
        ]
        
    def __str__(self) -> str:
        return self.title
    
    
class Commentary(models.Model):
    ...