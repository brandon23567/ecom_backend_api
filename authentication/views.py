from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import UserProfile
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["GET"])
def signup(request):
    return Response({ "message": "This is signup page" })



@api_view(["POST"])
def signup_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    user_profile_image = request.FILES.get("user_profile_image")
    
    if not username or not email or not password:
        return Response({ "message": "All inputs are required cuh" })
    
    
    new_user_instance = User.objects.create_user(username=username, email=email, password=password)
    new_user_instance.save()
    
    if new_user_instance:
        new_user_profile = UserProfile.objects.create(user=new_user_instance, profile_image=user_profile_image)
        new_user_profile.save()
        
        return Response({ "message": "New user profile has been created cuh" })
    

@api_view(["POST"])
def signin_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return Response({ "message": "All credentials are required chief" })
    
    try:
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({ "message": "You have been logged in g", "access_token": access_token })
        
    except user.DoesNotExist:
        return Response({ "message": "No such user" })
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    current_user = request.user
    
    if not current_user:
        return Response({ "message": "My g, u not logged in right now" })
    
    try:
        if current_user.is_authenticated:
            current_user_details = UserProfile.objects.get(user=current_user)
            if current_user_details:
                user_details = {
                    "username": current_user_details.user.username,
                    "profile_image_url": current_user_details.profile_image.url
                }
            return Response({ "current_user_details": user_details })
    except:
        return Response({ "message": "You are not logged in cuh" })