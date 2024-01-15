from rest_framework import serializers

from store.models import User, Category, Author, Book, Commentary


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ('id', 'username')


class BookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'publication_date', 
                  'created', 'updated', 'author', 'categories')
    

class CommentaryCreatOrReadSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(required=False)
    author = UserSerializer()
    
    class Meta:
        model = Commentary
        fields = ('author', 'text', 'created', 'updated', 'book_id')
        
    def create(self, validated_data):
        author_data = validated_data.pop('author')
        book_id = validated_data.pop('book_id')
        commentary = Commentary(**validated_data)
        commentary.author_id = author_data.get('id')
        commentary.book_id = book_id
        commentary.save()
        return commentary


class CommentaryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ('text',)
        
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', None)
        instance.save()
        return instance