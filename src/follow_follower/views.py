from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .models import FollowFollower
from Post.models import Post, PostImage , Like , Comment
from User.models import User

from .serializer import FollowSerializer , FollowerListSerializer , FollowingListSerializer , PostListSerializer

class FollowUser(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self , request , *args , **kwags):
        
        data = request.data

        follow_serializer = FollowSerializer(data = data)
        
        follow_to = data.get('follow_to')
        follow_by = request.user.id

        if follow_serializer.is_valid() :

            if follow_by == follow_to :
                return Response({"msg" : "Not Follow Yourself!"},status=status.HTTP_400_BAD_REQUEST)
            
            if FollowFollower.objects.filter(follow_by = follow_by , follow_to = follow_to).exists() :
                return Response({"msg" : "Already Follow"},status=status.HTTP_400_BAD_REQUEST)
            
            follow_serializer.save(follow_by = request.user)

            follow_to_user = User.objects.filter(id = follow_to).first()
            follower_by_user = User.objects.filter(id = follow_by).first()

            follow_to_user.follower_count += 1
            follower_by_user.following_count += 1
            follow_to_user.save()
            follower_by_user.save()

            return Response(follow_serializer.data,status=status.HTTP_201_CREATED)
        else :
            return Response(follow_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        

class UnfollowUserView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    def delete(self , request):
        follow_to_id = request.data.get('follow_to')

        user = request.user

        follow_data = FollowFollower.objects.filter(follow_to = follow_to_id , follow_by = user.id).first()            
        if follow_data is None :
            return Response({"msg" : f"You Not Follow {follow_to_id}"} , status=status.HTTP_404_NOT_FOUND)

        follow_data.delete()

        follow_to_user = User.objects.filter(id = follow_to_id).first()
        follower_by_user = User.objects.filter(id = user.id).first()

        follow_to_user.follower_count -= 1
        follower_by_user.following_count -= 1
        follow_to_user.save()
        follower_by_user.save()

        return Response({"msg":"unfollowed" },status=status.HTTP_200_OK)



        

class UserFollowView(APIView):

    def get(self , request , *args , **kwags):
        username = request.data.get('username')

        try : 
            user_data = User.objects.get(username = username)
        except User.DoesNotExist :
            return Response({"msg" : "User Not Found"} , status=status.HTTP_404_NOT_FOUND)


        following = FollowFollower.objects.filter(follow_by = user_data.id)     
        following_serializer = FollowingListSerializer(following, many=True)
        
        follower = FollowFollower.objects.filter(follow_to = user_data.id)     
        follower_serializer = FollowerListSerializer(follower, many=True)

        follower_count = user_data.follower_count
        following_count = user_data.following_count

        data = {
            "user_id" : user_data.id,
            "user_name" : user_data.username,
            "followers": follower_serializer.data,
            "followings" : following_serializer.data,
            "following_count" : following_count,
            "follower_count" : follower_count
            }
        
        return Response(data , status=status.HTTP_200_OK)
    

class HomeView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self ,request):

        user = request.user
        
        following = FollowFollower.objects.filter(follow_by = user)  

        posts_data = []

        for following_obj in following:
            posts = Post.objects.filter(author = following_obj.follow_to , status = "published")
            for post in posts:
                post_images = PostImage.objects.filter(post=post)
                like = Like.objects.filter(post=post)
                comment = Comment.objects.filter(post = post)
                posts_data.append((post, post_images,like,comment))

        posts_serializer = PostListSerializer(posts_data,many=True)


        data = {"posts" : posts_serializer.data}
        
        return Response(data , status=status.HTTP_200_OK)
    





    
        











