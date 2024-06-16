from django.db import models

# Create your models here.


class Question(models.Model):
    #user =
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True,null = True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title + ' ' + self.content
    
    
class Reply(models.Model):
    #user=
    question = models.ForeignKey(Question,related_name="replies",on_delete=models.CASCADE)
    content =  models.TextField(null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Reply to '{self.question.title}'"