from tkinter import CASCADE
from django.db import models

class FollowFollower(models.Model):
    follow_to = models.ForeignKey('User.User', related_name='following' , on_delete=models.CASCADE)
    follow_by = models.ForeignKey('User.User', related_name='followers' , on_delete=models.CASCADE , null =True)
    created_at = models.DateTimeField(auto_now_add=True , null=True)