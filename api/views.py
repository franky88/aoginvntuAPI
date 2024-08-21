from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from stuffs.models import Category, Unit, Unitkit, UnitStatus
from users.models import Department
from django.contrib.auth import get_user_model
from api.serializers import UnitModelSerializer, CategoryModelSerializer, UnitKitModelSerializer, UnitStatusModelSerializer, DepartmentModelSerializer, UserModelSerializer, MyTokenObtainPairSerializer, MyTokenVerifySerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.permissions import IsAuthenticated

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
        user = serializer.user

        print("User:", user)
        print("Tokens:", tokens)

        # Set the tokens as HttpOnly cookies
        res = Response({"success": True, "access": tokens['access']}, status=status.HTTP_200_OK)
        res.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,  # Ensure this is only sent over HTTPS
            samesite='None',
            max_age=3600,  # 1 hour for access token
        )
        res.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='None',
            max_age=604800,  # 1 week for refresh token
        )
        return res

class LogoutView(APIView):
    def post(self, request):
        response = Response({"Message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', samesite='Lax', secure=True)
        response.delete_cookie('refresh_token', samesite='Lax', secure=True)

        return response

class CurrentUserView(APIView):
    permission_classes = user_permissions

    def get(self, request):
        print(f"User: {request.user}")
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

class UnitkitViewset(viewsets.ModelViewSet):
    queryset = Unitkit.objects.all()
    serializer_class = UnitKitModelSerializer
    permission_classes = user_permissions

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentModelSerializer
    permission_classes = user_permissions