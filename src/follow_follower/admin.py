from django.contrib import admin
from .models import FollowFollower

# Register your models here.

@admin.register(FollowFollower)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id','follow_to','follow_by')