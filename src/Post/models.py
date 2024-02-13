from email.mime import image
from email.policy import default
from random import choices
from unittest.util import _MAX_LENGTH
from django.db import models

postChoices = {
    ("draft", "draft"),
    ("published","published"),
    ("private","private"),
}

def upload_image(instance , filename):
    user = instance.post.author.username
    return f'upload/{user}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # image = models.ImageField(upload_to=upload_image , null=True , blank=True)
    status = models.CharField(default = "published" , choices = postChoices , max_length = 10)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User.User", on_delete=models.CASCADE, related_name="blog_posts" ,null = True)
    updated_Posted = models.DateTimeField(auto_now_add=False , null=True)

    def __str__(self) -> str:
        return f"{self.title} | {self.author}"

class PostImage(models.Model):
    post = models.ForeignKey(Post ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image)
    created_at = models.DateTimeField(auto_now_add = True)
    
    
class PostPermission(models.Model):
    user = models.OneToOneField('User.User',on_delete=models.CASCADE)
    can_delete_post = models.BooleanField(default=True) 
    can_edit_post = models.BooleanField(default=True) 


class Like(models.Model):
    post = models.ForeignKey(Post ,on_delete=models.CASCADE ,related_name='post_likes')
    user = models.ForeignKey('User.User' ,on_delete=models.CASCADE ,related_name='user_like')
    like_at = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    post = models.ForeignKey(Post ,on_delete=models.CASCADE ,related_name='post_comment')
    user = models.ForeignKey('User.User' ,on_delete=models.CASCADE ,related_name='user_comment')
    comment = models.TextField()  
    comment_at = models.DateTimeField(auto_now_add = True)



