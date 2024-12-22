from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from users.models import User
from users.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny


# Create your views here
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully", "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Registration failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.get_user()
            user.last_login = timezone.now()
            user.save()
            tokens = serializer.get_tokens()
            return Response({"message": "Login successful", "access_token": tokens['access_token'], "refresh_token": tokens['refresh_token']}, status=status.HTTP_200_OK)
        return Response({"error": "Login failed", "details": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)



class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response({"message": "User data retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        if user != request.user:
            raise PermissionDenied("You do not have permission to update this user.")
        
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User data updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        if user != request.user:
            raise PermissionDenied("You do not have permission to delete this user.")

        user.delete()
        return Response({"message": "User successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

