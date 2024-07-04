from django.contrib import admin

from community.models import Category, Post, Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
