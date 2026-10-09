from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urljoin
import requests
from django.urls import reverse


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


from .models import User, ProviderProfile
from .serializers import UserSerializer, ProviderProfileSerializer


class UserAPIView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsergetAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        users = User.objects.all()
        search = request.query_params.get("search")
        if search:
            users =users.filter(
                Q(username__icontains=search)|
                Q(email__icontains=search)|
                Q(id__icontains=search)
            )
            

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class ProviderProfileView(APIView):
    def get(self,request):
        providers = ProviderProfile.objects.all()
        serializer = ProviderProfileSerializer(providers,  many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  

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


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):

        return Response(
            {"role":request.user.role,
             "id":request.user.id,
             "username": request.user.username,
             "email": request.user.email,})

    
class SelectRoleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
        })


    def post(self, request):

        role = request.data.get("role")

        if role not in ["user", "provider"]:
            return Response(
                {"error": "Invalid role"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user

        user.role = role
        user.save(update_fields=["role"])

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Role updated successfully",
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        If you are building a fullstack application (eq. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")
        print("code :", code)

        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Remember to replace the localhost:8000 with the actual domain name before deployment
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))

        response = requests.post(url=token_endpoint_url, data={"code": code})
        return Response(response.json(), status=status.HTTP_200_OK)
