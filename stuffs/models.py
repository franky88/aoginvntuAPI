from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

import uuid
import datetime

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=102)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    
class UnitStatus(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = 'unit statuses'

    def __str__(self):
        return self.name
    
class Unitkit(models.Model):
    kit_code = models.CharField(max_length=13, unique=True, null=True, blank=True)
    name = models.CharField(max_length=120)
    assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        data = "%s-%s"%(self.name, self.kit_code)
        return data
    
class Unit(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    barcode = models.CharField(max_length=60, unique=True, null=True, blank=True)
    name = models.CharField(max_length=120)
    model = models.CharField(max_length=60, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    date_purchased = models.DateField()
    cost = models.FloatField()
    serial = models.CharField(max_length=120, unique=True)
    unit_kit = models.ForeignKey(Unitkit, on_delete=models.SET_NULL, null=True, blank=True)
    item_status = models.ForeignKey(UnitStatus, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name.upper()
    

@receiver(pre_save, sender=Unitkit)
def unitkit_pre_save(sender, instance, *args, **kwargs):
    if not instance.kit_code:
        kit_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.kit_code = kit_code

@receiver(pre_save, sender=Unit)
def unit_pre_save(sender, instance, *args, **kwargs):
    if not instance.barcode:
        barcode = str(uuid.uuid4().int).replace("-", "").upper()[:13]
        instance.barcode = barcode