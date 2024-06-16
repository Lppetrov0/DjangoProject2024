from django.contrib import admin
from .models import Question,Reply
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import AppConfig
from django.contrib.auth.models import User,Group
# Register your models here.
admin.site.register(Question)
admin.site.register(Reply)


def create_group_perms():
    user_group,created  = Group.objects.get_or_create(name="NormalUser")
    
    moderator,created = Group.objects.get_or_create(name="Moderator")
    
    question_content = ContentType.objects.get_for_model(Question)
    reply_content = ContentType.objects.get_for_model(Reply)
    
    
    
    normal_perms =[
        Permission.objects.get(codename = 'view_question',content_type = question_content),
        Permission.objects.get(codename = 'view_reply',content_type = reply_content)
    ]
    
    user_group.permissions.set(normal_perms)
    
    moderator_permissions = [
        Permission.objects.get(codename='view_question', content_type=question_content),
        Permission.objects.get(codename='add_question', content_type=question_content),
        Permission.objects.get(codename='change_question', content_type=question_content),
        Permission.objects.get(codename='delete_question', content_type=question_content),
        Permission.objects.get(codename='view_reply', content_type=reply_content),
        Permission.objects.get(codename='add_reply', content_type=reply_content),
        Permission.objects.get(codename='change_reply', content_type=reply_content),
        Permission.objects.get(codename='delete_reply', content_type=reply_content),
    ]
    moderator.permissions.set(moderator_permissions)
    
        

class QuestionsConfig(AppConfig):
    name = 'questions'

    def ready(self):
        create_group_perms()

