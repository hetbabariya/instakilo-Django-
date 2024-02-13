from django.urls import path
from .views import CreateUser , LoginUser , LogoutUser , ChangePassword , ForgetPassword , DeleteUser , UpdateUser , SendOtp , VerifyOtp

urlpatterns = [
    path('create-user',CreateUser.as_view()),
    path('send_otp',SendOtp.as_view()),
    path('verify_otp',VerifyOtp.as_view()),
    path('login',LoginUser.as_view()),
    path('logout',LogoutUser.as_view()),
    path('change-password',ChangePassword.as_view()),
    path('forget-password',ForgetPassword.as_view()),
    path('delete-user',DeleteUser.as_view()),
    path('update-user',UpdateUser.as_view()),
]