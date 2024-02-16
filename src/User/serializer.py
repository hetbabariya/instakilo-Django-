from rest_framework import serializers

from User.models import User

class SearchUserSerializer(serializers.ModelSerializer):
    user_id  = serializers.SerializerMethodField()
    user_name  = serializers.SerializerMethodField()

    class Meta :
        model =  User
        fields= ('user_id', 'user_name')
    
    def get_user_id (self, obj) :
        return obj.id
    
    def get_user_name (self, obj) :
        return obj.username