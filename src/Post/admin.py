from csv import list_dialects
from django.contrib import admin

from .models import Post, PostPermission , PostImage , Like , Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('id' , 'title' , 'content' ,'status', 'date_posted' , 'updated_Posted' , 'author')
    list_filter = ('title','status')
    search_fields = ('status',)
    list_editable = ('status',)
    list_per_page = 10
    ordering = ('id',)


@admin.register(PostPermission)
class PostPermissionAdmin(admin.ModelAdmin):
    list_display = ('user' , 'can_delete_post' , 'can_edit_post')

    
@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post' , 'image' , 'created_at')

@admin.register(Like)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id','post' , 'user')

@admin.register(Comment)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id','post' , 'user' , 'comment')
