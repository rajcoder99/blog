from django.contrib import admin
from .models import Blog_post
# Register your models here.

@admin.register(Blog_post)
class PostMobelAdmin(admin.ModelAdmin):
    list_display = ['id','title','desc']