from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from stuffs.models import Category, Unit, Unitkit, UnitStatus, KitAssignment
from users.models import Department
from django.contrib.auth import get_user_model
from api.serializers import UnitModelSerializer, CategoryModelSerializer, UnitKitModelSerializer, UnitStatusModelSerializer, DepartmentModelSerializer, UserModelSerializer, MyTokenObtainPairSerializer, MyTokenVerifySerializer, KitAssignmentModelSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.filters import UnitFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from datetime import datetime


User = get_user_model()

user_permissions = [IsAuthenticated]

@api_view(['GET'])
def getRoutes(request):
    routes = [
        "/logout",
        "/token",
        "/token/refresh",
        "/token/verify",
    ]
    return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        # Set the tokens as HttpOnly cookies
        res = Response({"success": True}, status=status.HTTP_200_OK)
        res.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite='None',
            max_age=86400,
        )
        res.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='None',
            max_age=604800,
        )
        return res

class LogoutView(APIView):
    def post(self, request):
        response = Response({"Message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', samesite='None')
        response.delete_cookie('refresh_token', samesite='None')

        return response

class CurrentUserView(APIView):
    permission_classes = user_permissions

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)

class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer
    permission_classes = user_permissions

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = user_permissions

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def all(self, request):
        print(self.get_queryset())
        all = self.get_queryset().filter(is_active=True)

        page = self.paginate_queryset(all)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(all, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def working(self, request):
        print(self.get_queryset())
        working = self.get_queryset().filter(is_active=True, is_working=True)

        page = self.paginate_queryset(working)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(working, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def resigned(self, request):
        resigned = self.get_queryset().filter(is_active=True, is_working=False)

        page = self.paginate_queryset(resigned)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(resigned, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def archived(self, request):
        archived = self.get_queryset().filter(is_active=False, is_working=False)

        page = self.paginate_queryset(archived)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(archived, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET','POST'])
    def is_archived(self, request, pk=None):
        user = self.get_object()
        if not user.is_working:
            user.is_active = not user.is_active
        else:
            user.is_active = True
            user.is_working = False
        user.save()
        serializer = self.get_serializer(user)
        return Response({"User": serializer.data}, status=status.HTTP_200_OK)

        

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = user_permissions

class UnitStatusViewset(viewsets.ModelViewSet):
    queryset = UnitStatus.objects.all()
    serializer_class = UnitStatusModelSerializer
    permission_classes = user_permissions

class UnitViewset(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitModelSerializer
    permission_classes = user_permissions
    filterset_class = UnitFilter
    filter_backends = [DjangoFilterBackend]

    @action(detail=False)
    def working(self, request):
        working = self.get_queryset().filter(item_status__name="Working")

        page = self.paginate_queryset(working)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(working, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def maintenance(self, request):
        maintenance = self.get_queryset().filter(item_status__name="Maintenance")

        page = self.paginate_queryset(maintenance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(maintenance, many=True)
        return Response(serializer.data)

class UnitkitViewset(viewsets.ModelViewSet):
    queryset = Unitkit.objects.all()
    serializer_class = UnitKitModelSerializer
    permission_classes = user_permissions

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentModelSerializer
    permission_classes = user_permissions

class KitAssignmentViewset(viewsets.ModelViewSet):
    queryset = KitAssignment.objects.all()
    serializer_class = KitAssignmentModelSerializer
    permission_classes = user_permissions

    @action(detail=True, methods=['GET','POST'])
    def returned(self, request, pk=None):
        kit = self.get_object()
        if not kit.is_returned:
            kit.is_returned = not kit.is_returned
        kit.assign_to = None
        kit.date_returned = datetime.now().date()
        kit.is_available = True
        kit.save()
        serializer = self.get_serializer(kit)
        return Response({"Kit": serializer.data}, status=status.HTTP_200_OK)