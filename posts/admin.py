"""User admin classes"""

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Register your models here.

#Models
from django.contrib.auth.models import User
from posts.models import Post

# Register Profile
admin.site.register(Post)

