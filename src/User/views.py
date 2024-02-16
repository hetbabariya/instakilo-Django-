import datetime
import re
from tokenize import Token
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.paginator import Paginator

from random import randint
from datetime import datetime , timedelta

from django.core.mail import EmailMessage, get_connection
from django.conf import settings

from .models import Otp , User
from Post.models import PostPermission
from .serializer import SearchUserSerializer

class CreateUser(APIView):
    def post(self , request):
        data = request.data

        user_name = data['username']
        user_email = data['email']
        password = data['password']

        if User.objects.filter(username = user_name).exists():
            return Response({"message":"User already exists"},status=status.HTTP_400_BAD_REQUEST)
    
        
        user = User.objects.create(username = user_name , email = user_email)
        user.set_password(password)
        user.save()

        PostPermission.objects.create(user = user)

        return Response({'message': 'successfully created a new account'},status=200)


class SendOtp(APIView):
    def post(self , request):

        data = request.data

        user_email = data['email']

        user_data = User.objects.filter(email = user_email).first()

        if user_data is None :
            return Response({"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        otp = randint(100000 , 999999)

        with get_connection(  
            host=settings.EMAIL_HOST, 
            port=settings.EMAIL_PORT,  
            username=settings.EMAIL_HOST_USER, 
            password=settings.EMAIL_HOST_PASSWORD, 
            use_tls=settings.EMAIL_USE_TLS  
        ) as connection:  
            subject = "verifiy Account"
            email_from = settings.EMAIL_HOST_USER  
            recipient_list = [user_email]  
            message = f"Your Verification OTP code : {otp}"  
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send() 

        otp_data = Otp.objects.filter(user_id = user_data).first()
        if otp_data is None :
            otp_create = Otp.objects.create(otp = otp , user_id = user_data , otp_send_at = datetime.now())
            otp_create.save()
        else:
            otp_data.otp = otp
            otp_data.otp_send_at = datetime.now()
            otp_data.save()
        
        return Response({"message" : "Otp send Successfully"},status=status.HTTP_200_OK)



class VerifyOtp(APIView):

    def post(self , request):

        data = request.data

        user_email = data['email']    
        user_otp = data['otp']  

        user_data = User.objects.filter(email = user_email).first()

        if user_data is None :
            return Response({"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        otp_data = Otp.objects.filter(user_id = user_data).first()

        if otp_data.otp != user_otp :
            return Response({"error":"Wrong OTP entered!"},status=status.HTTP_401_UNAUTHORIZED)
        
        if datetime.now().replace(tzinfo=None) > (otp_data.otp_send_at + timedelta(minutes=3)).replace(tzinfo=None) :
            return Response({"error":"OTP has been expired! Please generate new OTP."},status=status.HTTP_410_GONE)
        
        return Response({"message":"otp verify successfully!"},status=status.HTTP_200_OK)

class LoginUser(APIView):
    
    def post(self , request):

        data = request.data

        user_name = data['username']
        password = data['password']

        try :
            user = User.objects.get(username = user_name)
        except User.DoesNotExist :
            return Response({"error":"user does not exist"},status=404)
        
        if authenticate(username = user_name , password = password):
            token , create = Token.objects.update_or_create(user=user)
            
            if not create :
                token.delete()
                token = Token.objects.create(user = user)
                return Response({'token' : token.key}, status=200)
                            
            return Response({'token': token.key})

        return Response({'error': 'Invalid credentials'}, status=401)


class LogoutUser(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def delete(self , request):
        Token.objects.get(user = request.user).delete()
        return Response({'message':'Logged out successfully'},status=200)
    
    
class ChangePassword(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self , request):

        data = request.data

        current_password = data['current_password']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        if authenticate(username = request.user.username , password = current_password):
            if new_password == confirm_password :
                request.user.set_password(new_password)
                request.user.save()
                return Response({'message':'Password changed Successfully'} , status=200)
            else:
                return Response({'error':'New Password and Confirm Password do not match'} , status=400)
        else :
            return Response({'error':'Current Password is Incorrect'} , status=status.HTTP_403_FORBIDDEN)

class ForgetPassword(APIView):
    
    def post(self , request):
        
        data = request.data
        
        email = data['email']
        otp = data['otp']
        new_password = data['new_password']
        
        user_data = User.objects.filter(email = email).first()

        if user_data is None :
            return Response({"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        otp_data = Otp.objects.filter(user_id = user_data).first()

        if otp_data.otp != otp :
            return Response({"error":"Wrong OTP entered!"},status=status.HTTP_401_UNAUTHORIZED)
        
        if datetime.now().replace(tzinfo=None) > (otp_data.otp_send_at + timedelta(minutes=3)).replace(tzinfo=None) :
            return Response({"error":"OTP has been expired! Please generate new OTP."},status=status.HTTP_410_GONE)
        
        user_data.set_password(new_password)
        user_data.save()

        return Response({'message':'New Password set Successfully'} , status=200)


class DeleteUser(APIView):
    authentication_classes = (TokenAuthentication,)
    
    def delete(self,request):

        try:
            User.objects.get(username = request.user.username).delete()
            return Response({"Message":"User has been deleted"},status=200)
        except User.DoesNotExist :
            return Response({"Error":"User does not exist"} , status=404)
        
class UpdateUser(APIView):
    authentication_classes = (TokenAuthentication,)
    pass



class SearchUserView(APIView):

    def get(self , request ):
        username = request.query_params.get('username')

        if username is None :
            return Response({"msg" : "None type User"} , status=status.HTTP_400_BAD_REQUEST)
        
        user_data = User.objects.filter(Q(username__contains = username)).all()
        # user_serializer = SearchUserSerializer(user_data , many = True)
        
        p = Paginator(user_data, 5)
        
        page_obj = p.page(1)
        
        user_serializer = SearchUserSerializer(page_obj, many=True)
        return Response({"user" : user_serializer.data}, status=status.HTTP_200_OK)