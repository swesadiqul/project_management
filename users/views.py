# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import authenticate
# from .models import User
# from .serializers import UserSerializer


# Create your views here.
# class RegisterUser(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginUser(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# class UserDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         user = User.objects.filter(id=id).first()
#         if not user:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

#     def put(self, request, id):
#         user = User.objects.filter(id=id).first()
#         if not user:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         user = User.objects.filter(id=id).first()
#         if not user:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
#         user.delete()
#         return Response({"message": "User deleted"}, status=status.HTTP_204_NO_CONTENT)


from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    def post(self, request):
        # Here you will handle JWT token generation
        user = User.objects.filter(email=request.data['username']).first()
        if user and user.password == request.data['password']:
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
