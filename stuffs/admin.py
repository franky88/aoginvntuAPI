from django.contrib import admin
from .models import Unit, Unitkit, Category, UnitStatus

# Register your models here.
admin.site.register(Unit)
admin.site.register(Unitkit)
admin.site.register(Category)
admin.site.register(UnitStatus)