from django.urls import path
from stuffs.views import dashboard, unit_page, unit_details

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('units', unit_page, name="unit_page"),
    path('units/<unit_id>', unit_details, name="unit_details"),
]