from django.urls import path, include
from rest_framework import routers
from api.views import UnitViewset, CategoryViewset, UnitkitViewset, UnitStatusViewset, getRoutes, DepartmentViewset, UserViewset, KitAssignmentViewset
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from api.views import MyTokenObtainPairView, LogoutView, CurrentUserView

router = routers.DefaultRouter()
router.register(r'users', UserViewset)
router.register(r'units', UnitViewset)
router.register(r'categories', CategoryViewset)
router.register(r'kits', UnitkitViewset)
router.register(r'unit-status', UnitStatusViewset)
router.register(r'departments', DepartmentViewset)
router.register(r'assignments', KitAssignmentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('current-user/', CurrentUserView.as_view(), name='current_user'),
    path('auth', getRoutes),
    path('auth/logout', LogoutView.as_view(), name='logout_user'),
    path('auth/token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
