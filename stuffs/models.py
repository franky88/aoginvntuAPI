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
    is_available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        data = "%s-%s"%(self.name, self.kit_code)
        return data
    
class Item(models.Model):
    create_by = models.ForeignKey(User, related_name="items", on_delete=models.SET_NULL, null=True, blank=True)
    barcode = models.CharField(max_length=60, unique=True, null=True, blank=True)
    name = models.CharField(max_length=120)
    model = models.CharField(max_length=60, null=True, blank=True)
    descriptions = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def item_name(self):
        name = "%s - (%s)"%(self.name, self.model)
        return name.upper()

    def __str__(self):
        return self.item_name()

class ItemTransaction(models.Model):
    process_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Item, related_name="item_transactions", on_delete=models.SET_NULL, null=True, blank=True)
    date_purchased = models.DateField(blank=True, null=True)
    cost = models.FloatField()
    quantity = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.item.name.upper()

class Unit(models.Model):
    item = models.ForeignKey(Item, related_name="units", on_delete=models.SET_NULL, null=True, blank=True)
    serial = models.CharField(max_length=120, unique=True)
    unit_kit = models.ForeignKey(Unitkit, related_name='units', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.item.name.title()
    
class ItemStatus(models.Model):
    item = models.ForeignKey(Item, related_name="item_status", on_delete=models.SET_NULL, null=True, blank=True)
    unit_status = models.ForeignKey(UnitStatus, related_name="item_status", on_delete=models.SET_NULL, null=True, blank=True)
    serial = models.CharField(max_length=120, unique=True)
    remarks = models.TextField(blank=True, null=True)
    date_reported = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.item.name.upper()
    
class KitAssignment(models.Model):
    unit_kit = models.ForeignKey(Unitkit, related_name="kit_assignments", on_delete=models.SET_NULL, null=True, blank=True)
    assign_to = models.ForeignKey(User, related_name="kit_assignments", on_delete=models.SET_NULL, null=True, blank=True)
    date_assigned = models.DateField()
    date_returned = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        assigned = "%s - %s"%(self.unit_kit, self.assign_to)
        return assigned


@receiver(post_save, sender=Unitkit)
def unitkit_postsave(sender, instance, created, *args, **kwargs):
    if created and not instance.kit_code:
        kit_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.kit_code = kit_code
        Unitkit.objects.filter(pk=instance.pk).update(kit_code=kit_code)

@receiver(post_save, sender=Item)
def item_postsave(sender, instance, created, *args, **kwargs):
    if created:
        instance.__item_status__unit_status__name = "working"
        instance.__item_status__item__id = instance.id
        instance.save()