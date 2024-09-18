from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from stuffs.models import (
    Category, 
    Unit, 
    Unitkit, 
    UnitStatus, 
    KitAssignment, 
    Item, 
    ItemTransaction,
    ItemStatus
    )
from users.models import Department
from django.contrib.auth import get_user_model
from api.serializers import (
    UnitModelSerializer,
    CategoryModelSerializer,
    UnitKitModelSerializer,
    UnitStatusModelSerializer,
    DepartmentModelSerializer,
    UserModelSerializer,
    MyTokenObtainPairSerializer,
    MyTokenVerifySerializer,
    KitAssignmentModelSerializer,
    ItemModelSerializer,
    ItemTransactionModelSerializer,
    ItemStatusModelSerializer
    )
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.filters import UnitFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from datetime import datetime


User = get_user_model()

user_permissions = [IsAuthenticated]

class UnitPagination(PageNumberPagination):
    page_size=10

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
    
    @action(detail=True, methods=['GET'])
    def unit_assignment(self, request, pk=None):
        user = self.get_object()
        kit_assignment = user.kit_assignments.filter(assign_to=user)
        if kit_assignment.exists():
            serializer = KitAssignmentModelSerializer(kit_assignment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No kit assignments found for this user."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['PUT'])
    def upload_edit_image(self, request, pk=None):
        user = self.get_object()
        if 'image' in request.FILES or None:
            user.image = request.FILES['image']
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = user_permissions

class ItemTransactionViewset(viewsets.ModelViewSet):
    queryset = ItemTransaction.objects.all()
    serializer_class = ItemTransactionModelSerializer
    permission_classes = user_permissions
    
class ItemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    permission_classes = user_permissions

    @action(detail=False)
    def available(self, request):
        item_available = self.get_queryset().filter(item_transactions__quantity__gte=1)

        page = self.paginate_queryset(item_available)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(item_available, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def update_quantity_sub(self, request, pk=None):
        item = self.get_object()
        item.item_transactions.update(quantity=F('quantity') - 1)
        serializer = self.get_serializer(item)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'])
    def update_quantity_add(self, request, pk=None):
        item = self.get_object()
        item.item_transactions.update(quantity=F('quantity') + 1)
        serializer = self.get_serializer(item)
        return Response(serializer.data)


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
    pagination_class = UnitPagination

    # @action(detail=False)
    # def working(self, request):
    #     return self._filter_by_status("working")
    
    # @action(detail=False)
    # def maintenance(self, request):
    #     return self._filter_by_status("maintenance")
    
    # @action(detail=False)
    # def not_working(self, request):
    #     return self._filter_by_status("not working")

    # def _filter_by_status(self, status_name):
    #     queryset = self.get_queryset().filter(unit_status__name=status_name)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

class UnitkitViewset(viewsets.ModelViewSet):
    queryset = Unitkit.objects.all()
    serializer_class = UnitKitModelSerializer
    permission_classes = user_permissions

    @action(detail=True, methods=['POST'])
    def assign_unit_kit(self, request, pk=None):
        unit_kit = self.get_object()

        unit_kit.is_available = False
        unit_kit.save()

        serializer = UnitKitModelSerializer(unit_kit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['PUT'])
    def return_assign_unit_kit(self, request, pk=None):
        unit_kit = self.get_object()

        unit_kit.is_available = True
        unit_kit.save()

        if unit_kit.kit_assignments.exists():
            for assignment in unit_kit.kit_assignments.all():
                assignment.is_available = True
                assignment.is_returned = True
                assignment.assign_to = None
                assignment.unit_kit = None
                assignment.date_returned = datetime.now().date()
                assignment.save() 

        serializer = UnitKitModelSerializer(unit_kit)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def get_unit_list(self, request, pk=None):
        kit = self.get_object()

        units = kit.units.filter(unit_kit=kit.id)

        print("units: ", units)

        serializer = UnitModelSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def kit_unit_belong_to(self, request, pk=None):
        unit_kit = self.get_object()
        
        kit_assignments = unit_kit.kit_assignments.filter(unit_kit=unit_kit)
        
        if not kit_assignments.exists():
            return Response({"detail": "No kit assignments found for this unit kit."}, status=status.HTTP_404_NOT_FOUND)
        
        kit_assignment = kit_assignments.first()
        
        serializer = KitAssignmentModelSerializer(kit_assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def get_all_units(self, request, pk=None):
        unit_kit = self.get_object()
        units = unit_kit.units.all()
        serlializer = UnitModelSerializer(units, many=True)
        return Response(serlializer.data)
    
class ItemStatusViewset(viewsets.ModelViewSet):
    queryset = ItemStatus.objects.all()
    serializer_class = ItemStatusModelSerializer
    permission_classes = user_permissions

class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentModelSerializer
    permission_classes = user_permissions

class KitAssignmentViewset(viewsets.ModelViewSet):
    queryset = KitAssignment.objects.all().order_by('-id')
    serializer_class = KitAssignmentModelSerializer
    permission_classes = user_permissions