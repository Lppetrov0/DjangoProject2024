from django.contrib import admin
from .models import Question,Reply,User
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import AppConfig
from django.contrib.auth.models import User,Group
# Register your models here.
admin.site.register(Question)
admin.site.register(Reply)


