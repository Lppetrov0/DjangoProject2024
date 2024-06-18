from .models import Question,Reply
from .serializers import QuestionSerializer,ReplySerializer,RegisterSerializer,EditProfileSerializer,UserSerializer,LoginSerializer
from django.shortcuts import render 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate,logout
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

def mainpage(request):
    return render(request,'questions/mainpage.html')


@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    try:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, email=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            login(request, user)
            return Response({'detail': 'Successfully logged in.'})
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except AuthenticationFailed as e:
        return Response({'detail':str(e) }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({'detail': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@login_required
def logout_view(request):
    logout(request)
    return Response({'message': 'Successfully logged out.'})

@api_view(['PUT'])
@login_required
def edit_profile_view(request):
    if not request.user.is_authenticated:
        return Response({'message': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)
    serializer = EditProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@login_required
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
@login_required     
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
@login_required
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
@login_required
def reply_specific(request,question_id,reply_id):
    try: 
        reply = Reply.objects.get(pk = reply_id)
    except Reply.DoesNotExist or Question.DoesNotExist:
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