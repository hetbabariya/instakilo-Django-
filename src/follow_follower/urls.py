from django.urls import URLPattern, path

from .views import FollowUser , UserFollowView ,HomeView , UnfollowUserView

urlpatterns = [
    path('follow-user/',FollowUser.as_view()),
    path('unfollow/',UnfollowUserView.as_view()),
    path('get_user/',UserFollowView.as_view()),
    path('home_posts/',HomeView.as_view()),

]