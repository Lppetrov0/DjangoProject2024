from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=200)
    bio = models.TextField(max_length=2000,blank=True,null=True)
    
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email","password"]
    
    def __str__(self):
      return self.username


class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='questions') 
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,null = True)
    attachment = models.FileField(upload_to='attachemnts/',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} by {self.user.username}"
    

    
    
class Reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='replies')
    question = models.ForeignKey(Question,related_name="replies",on_delete=models.CASCADE)
    content =  models.TextField(null=False,blank=False)
    attachment = models.FileField(upload_to='attachemnts/',null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reply to '{self.question.title}' by {self.user.username}"