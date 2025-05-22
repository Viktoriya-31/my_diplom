from django.contrib import admin
from .models import Post, Comment, Like

admin.register(Post)
admin.register(Comment)
admin.register(Like)

