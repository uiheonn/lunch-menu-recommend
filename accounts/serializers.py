from rest_framework import serializers
#from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
#JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


User = get_user_model()

class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    nickName = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    re_password = serializers.CharField(required=True)
    
    #token, _ = Token.objects.get_or_create(user=user)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            nickName=validated_data['nickName'], 
        )
        

        user.set_password(validated_data['password']) 
        
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        token1, _ = Token.objects.get_or_create(user=user)

        if user is None:
            return {
                'email': 'None'
            }
        try:
            #payload = JWT_PAYLOAD_HANDLER(user)
            #wt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': token1.key
        }

        