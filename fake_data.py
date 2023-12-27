from store.models import Category, Author, Book
import random

categories = [Category(name=f'Категория {i}') for i in range(1, 5)]
author = [Author(name=f'Имя автора {i}') for i in range(1, 10)]

[i.save() for i in categories]
[i.save()for i in author]
    
for i in range(1, 21):
    book_auth = author[random.randint(0, 8)]
    book_cat = categories[random.randint(0, 3)]
    title = f'Название {i}'
    description = f'Описание {i}'
    publication_date = '2022-01-01'
    book = Book(title=title, description=description, publication_date=publication_date)
    book.save()
    book.author.add(book_auth)
    book.categories.add(book_cat)
    book.save()