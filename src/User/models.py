from email.policy import default
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    post_count = models.PositiveIntegerField(default = 0)
    follower_count = models.PositiveIntegerField(default = 0)
    following_count = models.PositiveBigIntegerField(default = 0)


class Otp(models.Model):
    otp = models.CharField(max_length = 6)
    otp_send_at = models.DateTimeField()
    user_id = models.ForeignKey("User.User",on_delete = models.CASCADE , related_name = "user_otp")

    def __str__(self) -> str:
        return f"{self.otp} | {self.user_id}"