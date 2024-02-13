from Post.models import PostPermission
from django.contrib.auth.models import User

users = User.objects.all()

for user in users:
    PostPermission.objects.update_or_create(user = user)

