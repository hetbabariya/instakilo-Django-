from dataclasses import field
from rest_framework import serializers
from .models import Post, PostImage ,Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta :
        model = Post
        fields = '__all__'

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostImage
        fields='__all__'

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post','comment']