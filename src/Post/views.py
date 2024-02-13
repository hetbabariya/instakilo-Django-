from datetime import datetime , timezone
from urllib import request, response

# from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import is_valid_path
from .models import Post, PostPermission , Like , Comment
from User.models import User
from .serializer import PostImageSerializer, PostSerializer , PostCommentSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser , IsAuthenticatedOrReadOnly , IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .userPostPermission import PostDeletePermission

@api_view(['GET'])
def get_posts(request):

    posts = Post.objects.all()
    data = []

    for post in posts :
        author_username = post.author.username if post.author else None

        context = {
            'title' : post.title,
            'content' : post.content,
            'date_posted' : post.date_posted,
            'author' : author_username,
            'updated_Posted' : post.updated_Posted
        }

        data.append(context)
    return Response(data)

@api_view(['POST'])
def create_post(request):
    data = request.data

    post_title = data.get('title')
    post_content = data.get('content')
    
    if request.user.is_authenticated:
        post_data = Post.objects.create(title=post_title, content=post_content, author=request.user)
    else:
        post_data = Post.objects.create(title=post_title, content=post_content, author=None)

    post_data.save()

    return Response({"message" : "post created"},status.HTTP_201_CREATED)


@api_view(['PATCH'])
def update_post(request):
    data = request.data

    post_id = data.get('id')
    
    try :
        Post_data = Post.objects.get(pk = post_id)
    except Post.DoesNotExist :
        return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
    
    if data.get('title'):
        Post_data.title = data['title']
    if data.get('content'):
        Post_data.content = data['content']

    Post_data.updated_Posted = datetime.now()
    Post_data.save()

    return Response({"message" : "post Updated"},status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_post(request):
    data = request.data

    post_id = data.get('id')

    try :
        Post_data = Post.objects.get(pk = post_id)
    except Post.DoesNotExist :
        return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
    
    Post_data.delete()

    return Response({"message" : "post Deleted"},status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def post_operations(request):

    if request.method == 'GET':
        post_id = request.query_params.get('id')
        search_by = request.query_params.get('title')

        if post_id:

            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({"message": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif search_by :
            post = Post.objects.filter(title__contains = search_by)

            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else :
            return Response({"message": "Data is Required"}, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'POST':
        data = request.data

        serializer = PostSerializer(data=data)

        user = User.objects.filter(username = "admin").first()

        if serializer.is_valid():
            serializer.save(author = user)
            return Response({"message" : "post created"},status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        data = request.data


        post_id = data.get('id')

        if not post_id :
            return Response({"message" : "is is required"},status=status.HTTP_400_BAD_REQUEST)
        
        Post_data = Post.objects.get(pk = post_id)
        serializer = PostSerializer(instance=Post_data,data=data , partial = True)

        if serializer.is_valid():
            serializer.save(updated_Posted = datetime.now())
            return Response({"message" : "post Updated"},status.HTTP_200_OK)
        else :
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post_id = request.query_params.get('id')

        try :
            Post_data = Post.objects.get(pk = post_id)
        except Post.DoesNotExist :
            return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
        
        Post_data.delete()

        return Response({"message" : "post Deleted"},status.HTTP_204_NO_CONTENT)


class PostOperations(APIView):

    permission_classes = [PostDeletePermission]
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAuthenticated   ]
    authentication_classes = (TokenAuthentication,)

    def get(self , request):

        post_id = request.query_params.get('id')
        search_by = request.query_params.get('title')

        if post_id:

            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                return Response({"message": "Data Not Found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif search_by :
            post = Post.objects.filter(title__contains = search_by)

            serializer = PostSerializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else :
            return Response({"message": "Data is Required"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self,request):
        data = request.data

        serializer = PostSerializer(data=data)

        # user = User.objects.filter(username = "admin").first()

        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response({"message" : "post created"},status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self,request):
        data = request.data


        post_id = data.get('id')

        if not post_id :
            return Response({"message" : "is is required"},status=status.HTTP_400_BAD_REQUEST)
        
        Post_data = Post.objects.get(pk = post_id)
        serializer = PostSerializer(instance=Post_data,data=data , partial = True)

        if serializer.is_valid():
            serializer.save(updated_Posted=datetime.now())
            return Response({"message" : "post Updated"},status.HTTP_200_OK)
        else :
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        post_id = request.query_params.get('id')

        try :
            Post_data = Post.objects.get(pk = post_id)
        except Post.DoesNotExist :
            return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
        
        Post_data.delete()

        return Response({"message" : "post Deleted"},status.HTTP_204_NO_CONTENT)



# create post
    
class CreatePost(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request , *args , **kwags):
        data = request.data
        user = request.user

        post_serializer = PostSerializer(data = data)
        if post_serializer.is_valid():
            post_serializer.save(author = request.user)

            image_data = {
                "image" : request.data.get('image'),
                "post" : post_serializer.data.get("id")
            }

            image_serializer = PostImageSerializer(data = image_data)

            if image_serializer.is_valid():
                image_serializer.save()
            else : 
                return Response(image_serializer.error , status=status.HTTP_400_BAD_REQUEST)
            
            user_data = User.objects.filter(id = user.id).first()
            
            user_data.post_count += 1
            user_data.save()

                        
            response = {}

            response.update(post_serializer.data)
            response.update(image_serializer.data)
            return Response(response , status=status.HTTP_201_CREATED)
        
        else : 
            return Response(post_serializer.errors , status=status.HTTP_400_BAD_REQUEST)




class PostImageOperation(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request , *args , **kwags):

        post_id = request.data.get('post')

        try:
            post = Post.objects.get(id = post_id)   
        except Post.DoesNotExist :
            return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
        
        PostSerializer = PostImageSerializer(data = request.data)
        if PostSerializer.is_valid():
            PostSerializer.save()
            return Response({"post" : PostSerializer.data} , status=status.HTTP_200_OK)
        return  Response(PostSerializer.errors , status=status.HTTP_400_BAD_REQUEST)
    


class PostLike(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self , request ):
        
        post_id = request.data.get('post')

        user = request.user

        try:
            post = Post.objects.get(id = post_id)   
        except Post.DoesNotExist :
            return Response("Post Does Not Exist!" , status.HTTP_404_NOT_FOUND)
        
        is_liked = Like.objects.filter(user=user, post=post).exists()

        if is_liked :
            return Response({"msg" : "Already Liked!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        like = Like(user = user , post = post )
        like.save()

        return Response({'msg':'Liked!'},status=status.HTTP_201_CREATED)  


class PostComment(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self , request):

        data = request.data

        user = request.user

        post_comment_serializer = PostCommentSerializer(data = data)

        if post_comment_serializer.is_valid() :
            comment = post_comment_serializer.save(user = user)
            return Response({"msg" : "commented!"} , status=status.HTTP_201_CREATED)   
        else : 
            return Response(post_comment_serializer.errors , status=status.HTTP_400_BAD_REQUEST)