from django.http import JsonResponse
from .models import Question,Reply
from .serializers import QuestionSerializer,ReplySerializer
from django.shortcuts import render 
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import login, authenticate,logout
from rest_framework import status
from django.contrib.auth.decorators import login_required,permission_required
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
# Create your views here.

def mainpage(request):
    return render(request,'questions/mainpage.html')


@api_view(['POST'])
def register(request):
  serializer = UserRegistrationSerializer(data = request.data)
  if serializer.is_valid():
      serializer.save()
      return Response(serializer.data,status = status.HTTP_201_CREATED)
  return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return Response({'message':'login successful'},status = status.HTTP_200_OK)
    return Response({'message':'login failed'},status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message':'logout successful'},status = status.HTTP_200_OK)

@api_view(['GET','POST'])
def user_profile(request):
    if request.method == 'GET':
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)
    elif request.method in ['PUT','PATCH']:
        partial = request.method == 'PATCH'
        serializer = CustomUserSerializer(request.user,data=request.data,partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        request.user.delete()
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def questions(request):
    if request.method == 'GET':
      question = Question.objects.all()
      serializer = QuestionSerializer(question,many = True)
      return Response(serializer.data)
    
      
    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','PUT','PATCH','DELETE'])     
def questions_specific(request,id):
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
       return Response(status = status.HTTP_404_NOT_FOUND)
    
    
    if request.method == 'GET':
       serializer = QuestionSerializer(question)
       return Response(serializer.data)
    elif request.method == 'PATCH':
       serializer = QuestionSerializer(question, data=request.data, partial=True)
       if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    elif request.method == 'PUT':
        serializer = QuestionSerializer(question,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    
    
@api_view(['POST'])    

def add_reply(request,question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = ReplySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(question = question)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET','PUT','PATCH','DELETE'])
def reply_specific(request,question_id,reply_id):
    try: 
        reply = Reply.objects.get(pk = reply_id)
    except Reply.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ReplySerializer(reply)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer  =  ReplySerializer(reply,data = request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer  =  ReplySerializer(reply,data = request.data,partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reply.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)