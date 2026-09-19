from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import User, ProviderProfile
from .serializers import UserSerializer, ProviderProfileSerializer


class UserAPIView(APIView):

    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserByIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self, request, id): 
        user = User.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderProfileByIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,user_id):
        provider = ProviderProfile.objects.get(user_id=user_id)
        serializer = ProviderProfileSerializer(provider)
        return Response(serializer.data, status=status.HTTP_200_OK)
     
    def patch(self, request, user_id):
        user = ProviderProfile.objects.get(user=user_id)
        serializer = ProviderProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors) 
