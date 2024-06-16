from django.db import models

# Create your models here.

# 
class Question(models.Model):
    #inquirer = 
    title = models.CharField(max_length= 150)
    description = models.TextField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Answer(models.Model):
    #user = 
    title_method = models.CharField(max_length= 150)
    answer = models.TextField(blank = False, null = False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title_method