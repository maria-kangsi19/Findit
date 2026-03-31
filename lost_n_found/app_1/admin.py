from django.contrib import admin
from .models import Category, Post, Message, Profile

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Profile)