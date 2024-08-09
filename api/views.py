from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from stuffs.models import Category, Unit, Unitkit, UnitStatus
from users.models import Department
from django.contrib.auth import get_user_model
from api.serializers import UnitModelSerializer, CategoryModelSerializer, UnitKitModelSerializer, UnitStatusModelSerializer, DepartmentModelSerializer, UserModelSerializer
from rest_framework.decorators import api_view

User = get_user_model()

@api_view(['GET'])
def getRoutes(request):
    routes = [
        "/token",
        "/token/refresh",
        "/token/verify",
    ]
    return Response(routes)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

class UnitStatusViewset(viewsets.ModelViewSet):
    queryset = UnitStatus.objects.all()
    serializer_class = UnitStatusModelSerializer

class UnitViewset(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitModelSerializer

class UnitkitViewset(viewsets.ModelViewSet):
    queryset = Unitkit.objects.all()
    serializer_class = UnitKitModelSerializer

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentModelSerializer