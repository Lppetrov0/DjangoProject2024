from rest_framework import serializers
from .models import Question,Reply,User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        return user

class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id','user','title','content','attachment','created','update']
        
        
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id','user','content','attachment','created','update']
    
    
        