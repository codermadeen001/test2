from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
import random
import string
from django.shortcuts import render

User = get_user_model()

def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"success": False, "message": "Email and password are required"}, status=400)

    user = authenticate(request, email=email, password=password)
    if not user:
        return Response({"success": False, "message": "Invalid credentials!"}, status=401)

    # Generate token
    token = generate_token(user)
    
    # Prepare user data to return
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
    }
    
    # Return response with user data
    return Response({
        "success": True, 
        "token": token, 
        "role": user.role,
        "user": user_data
    }, status=200)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_agent(request):
    """Create a new agent (admin only)"""
    # Get data from request
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Validate required fields
    if not name or not email or not password:
        return Response({
            "success": False, 
            "message": "Name, email and password are required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        return Response({
            "success": False, 
            "message": "User with this email already exists"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Create the agent
        agent = User.objects.create(
            name=name,
            email=email,
            password=make_password(password),  
            role='agent'
        )
        
        return Response({
            "success": True,
            "message": "Agent created successfully",
            "user": {
                "id": agent.id,
                "name": agent.name,
                "email": agent.email,
                "role": agent.role,
                "created_at": agent.created_at.strftime('%Y-%m-%d %H:%M:%S') if agent.created_at else None
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            "success": False,
            "message": f"Error creating agent: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    
    users = User.objects.all().values('id', 'name', 'email', 'role', 'created_at')
    return Response({'users': list(users)})