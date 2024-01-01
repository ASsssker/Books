from django.contrib import admin
from .models import Category, Book, Author, Commentary

# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Commentary)