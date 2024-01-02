from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Author, Category, Book, Commentary, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username',)


class CategoryAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    
    class Meta:
        model = Category
        fields  = ('id', 'name')


class AuthorAddSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    
    class Meta:
        model = Author
        fields  = ('id', 'name')


class CommentReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Commentary
        fields = ('author', 'text', 'created', 'updated')


class BookSerializer(serializers.ModelSerializer):
    author = AuthorAddSerializer(many=True, required=False)
    categories = CategoryAddSerializer(many=True, required=False)
    commentary = CommentReadSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'description', 'publication_date', 
                  'created', 'updated', 'categories', 'commentary')
        
        
    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        categories_data = validated_data.pop('categories', None)
        
        self.instance = Book.objects.create(**validated_data)
        self.instance.save()
        
        if author_data:
            authors = [Author.objects.get(**data) for data in author_data]
            self.instance.author.add(*authors)

        if categories_data:
            categories = [Category.objects.get(**data) for data in categories_data]
            self.instance.categories.add(*categories)
            
        return self.instance
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        categories_data = validated_data.pop('categories', None)
        instance.author.clear()
        instance.categories.clear()
        instance.__dict__.update(validated_data)
        
        if author_data:
            authors = [Author.objects.get(**data) for data in author_data]
            instance.author.add(*authors)
            
        if categories_data:
            categories = [Category.objects.get(**data) for data in categories_data]
            instance.categories.add(*categories)
        
        instance.save()
        return instance
        
        
class CategoryCreareOrReadSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'books')

        
class CommentaryCreatOrReadSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(required=False)
    author = UserSerializer()
    
    class Meta:
        model = Commentary
        fields = ('author', 'text', 'created', 'updated', 'book_id')
        
    def create(self, validated_data):
        print(validated_data)
        author_data = validated_data.pop('author')
        book_id = validated_data.pop('book_id')
        author = get_object_or_404(User, **author_data)
        commentary = Commentary(**validated_data)
        commentary.author = author
        commentary.book_id = book_id
        commentary.save()
        return commentary
    
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', None)
        instance.save()
        return instance
        
