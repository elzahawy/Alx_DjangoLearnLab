from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import RegisterSerializer, LoginSerializer
from .models import CustomUser


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=400)

        request.user.following.add(target_user)
        return Response({"detail": f"You are now following {target_user.username}."})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

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
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    """
    Retrieve the profile of the currently authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, "bio", ""),
            "followers": user.followers.count()
        }
        return Response(data)
