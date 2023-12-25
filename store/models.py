from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    file = models.FileField(upload_to='books/%Y/%m/%d/')
    Publication_date = models.DateField()
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
    
    
class Commentary(models.Model):
    ...