from django.contrib import admin

# Register your models here.
from .models import Post, Thread, Board

# How to show Post model in admin view
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'thumbnail', 'original') 

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'board', 'created_at') 

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at') 

admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Board, BoardAdmin)
