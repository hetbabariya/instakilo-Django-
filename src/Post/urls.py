from django.urls import path
from .views import  (
    get_posts ,
    create_post ,
    update_post,
    delete_post,
    post_operations,
    PostOperations,
    PostImageOperation,
    CreatePost,
    PostComment,
    PostLike,
    )

urlpatterns = [
    path('', get_posts),
    path('create/',create_post),
    path('update/',update_post),
    path('delete/',delete_post),
    path('operations/',post_operations),
    path('class-based-view/',PostOperations.as_view()),
    path('post-image/',PostImageOperation.as_view()),
    path('create_post/',CreatePost.as_view()),
    path('post-like/',PostLike.as_view()),
    path('post-comment/',PostComment.as_view()),
]