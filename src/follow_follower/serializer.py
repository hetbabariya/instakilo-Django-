from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers

from Post.models import Post ,  PostImage

from .models import FollowFollower

class  FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowFollower
        fields = '__all__'


class FollowingListSerializer(serializers.ModelSerializer):
    user_id  = serializers.SerializerMethodField()
    user_name  = serializers.SerializerMethodField()

    class Meta :
        model =  FollowFollower
        fields= ('user_id', 'user_name')
    
    def get_user_id (self, obj) :
        return obj.follow_to.id
    
    def get_user_name (self, obj) :
        return obj.follow_to.username

class FollowerListSerializer(serializers.ModelSerializer):
    user_id  = serializers.SerializerMethodField()
    user_name  = serializers.SerializerMethodField()

    class Meta :
        model =  FollowFollower
        fields= ('user_id', 'user_name')
    
    def get_user_id (self, obj) :
        return obj.follow_by.id
    
    def get_user_name (self, obj) :
        return obj.follow_by.username
    
        
class PostListSerializer(serializers.Serializer):
    user_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    caption = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        return obj[0].author.id

    def get_user_name(self, obj):
        return obj[0].author.username

    def get_title(self, obj):
        return obj[0].title 

    def get_caption(self, obj):
        return obj[0].content 

    def get_image(self, obj):
        return [img.image.url for img in obj[1]] 

    def get_like_count(self,obj):
        return obj[2].count()
            
    def get_comment_count(self,obj):
        return obj[3].count()

