from django.contrib import admin

# Register your models here.
from .models import Post
from .models import Thread

# How to show Post model in admin view
class PostAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'created_at', 'caption', 'text', 'original') 

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at') 

admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)
