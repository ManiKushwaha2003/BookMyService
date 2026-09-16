from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import ServiceSerializer
from .models import Service


class ServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        service = Service.objects.all()
        serializer = ServiceSerializer(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

class ServiceByIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id):
        service = Service.objects.get(id=id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request,id):
        service = Service.objects.get(id=id)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ServiceSerializer.data, status=status.HTTP_200_OK)  
        return Response(serializer.errors)


    def delete(self,request,id):
        service = Service.objects.get(id=id)  
        service.delete()
        return Response({"msg":"data deleted"}, status=status.HTTP_204_NO_CONTENT)