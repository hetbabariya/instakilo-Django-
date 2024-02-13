from django.contrib import admin
from User.models import Otp , User

admin.site.register(Otp)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','is_staff','post_count','follower_count','following_count')