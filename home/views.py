from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
questions = [
    {'id':1, 'title' : 'math' },
    {'id':2, 'title' : 'physics' },
    {'id':3, 'title' : 'chemistry' },
    {'id':4,'title' : 'biology' },
]



def home (request):
    return render(request, 'home.html',context)



def question(request,pk):
    question = None
    for i in questions:
        if i['id'] == int(pk):
            question = i
    context = {'question': question}
    return render(request, 'posts.html',context)



questions = [
    {'id':1, 'title' : 'math' },
    {'id':2, 'title' : 'physics' },
    {'id':3, 'title' : 'chemistry' },
    {'id':4,'title' : 'biology' },
]
context = {'questions':questions}
