from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
from .models import CustomUser


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)
        request.user.following.add(target_user)
        return Response({"detail": f"You are now following {target_user.username}."})

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=400)
        request.user.following.remove(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."})




class RegisterView(APIView):
    """
    Register a new user and return their token.
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    """
    Authenticate a user and return their token.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data  # LoginSerializer returns user object
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    """
    Retrieve the profile of the currently authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Make sure your CustomUser model has bio and followers fields
        data = {
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, "bio", ""),  # fallback if bio is missing
            "followers": getattr(user, "followers", []).count() if hasattr(user, "followers") else 0
        }
        return Response(data)







'''from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "followers": user.followers.count()
        }
        return Response(data)


# Create your views here.
'''
