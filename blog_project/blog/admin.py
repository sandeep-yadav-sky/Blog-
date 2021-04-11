from django.contrib import admin
from .models import post

@admin.register(post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','desc']
