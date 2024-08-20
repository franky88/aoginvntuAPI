from django.urls import path, include
from rest_framework import routers
from api.views import UnitViewset, CategoryViewset, UnitkitViewset, UnitStatusViewset, getRoutes, DepartmentViewset, UserViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewset)
router.register(r'units', UnitViewset)
router.register(r'categories', CategoryViewset)
router.register(r'kits', UnitkitViewset)
router.register(r'unit-status', UnitStatusViewset)
router.register(r'department', DepartmentViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth', getRoutes),
    path('auth/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
