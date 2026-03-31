from rest_framework import serializers
from .models import Category, User, Post, Message

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'post_type', 'description', 'category', 'category_name', 'reward', 'image', 'user', 'user_id', 'user_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_id', 'user_name', 'category_name']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


   
  