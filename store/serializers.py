from rest_framework import serializers
from rest_framework.fields import empty
from .models import Author, Category, Book


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


class BookCreateOrReadSerializer(serializers.ModelSerializer):
    author = AuthorAddSerializer(many=True)
    categories = CategoryAddSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'description', 'publication_date', 
                  'created', 'updated', 'categories')
        
        
    def create(self, validated_data):
        author_data = validated_data.pop('author', None)
        categories_data = validated_data.pop('categories', None)
        
        if author_data:
            authors = [Author.objects.get(**data) for data in author_data]
        if categories_data:
            categories = [Category.objects.get(**data) for data in categories_data]
            
        self.instance = Book.objects.create(**validated_data)
        self.instance.save()
        self.instance.author.add(*authors)
        self.instance.categories.add(*categories)
        return self.instance
    
    
class BookUpdateSerializer(serializers.ModelSerializer):
    author = AuthorAddSerializer(many=True)
    categories = CategoryAddSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'description', 'publication_date', 
                  'created', 'updated', 'categories')
        
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        categories_data = validated_data.pop('categories', None)
        
        if author_data:
            authors = [Author.objects.get(**data) for data in author_data]
        if categories_data:
            categories = [Category.objects.get(**data) for data in categories_data]
            
        instance.author.clear()
        instance.categories.clear()
        
        instance.__dict__.update(validated_data)
        instance.author.add(*authors)
        instance.categories.add(*categories)
        instance.save()
        return instance
        
        
class CategoryCreareOrReadSerializer(serializers.ModelSerializer):
    books = BookCreateOrReadSerializer(many=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'books')
    