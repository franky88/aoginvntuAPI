from rest_framework import serializers
from stuffs.models import (
    Unit, 
    Unitkit, 
    Category, 
    UnitStatus, 
    KitAssignment, 
    Item,
    ItemTransaction,
    ItemStatus
    )
from users.models import Department
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
import uuid

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

class MyTokenVerifySerializer(TokenVerifySerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = f"{user.first_name} {user.last_name}"
        return token

class DepartmentModelSerializer(serializers.ModelSerializer):
    profile_count = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ['id', 'name', 'profile_count']

    def get_profile_count(self, obj):
        return User.objects.filter(department=obj).count()

class UserModelSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'position', 'contact', 'birth_date', 'is_superuser', 'is_staff', 'employee_id', 'is_active', 'is_working', 'department', 'image', 'last_login']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = f"{instance.first_name} {instance.last_name}"
        return representation

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'create_by', 'barcode', 'name', 'model', 'descriptions', 'category']

class ItemTransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTransaction
        fields = ['id', 'process_by', 'item', 'date_purchased', 'cost', 'quantity', 'created', 'updated']

class UnitStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitStatus
        fields = ['id', 'name']

class ItemStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemStatus
        fields = ['id', 'item', 'unit_status', 'serial', 'remarks', 'date_reported', 'updated']

class UnitKitModelSerializer(serializers.ModelSerializer):
    kit_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Unitkit
        fields = ['id', 'name', 'kit_code', 'history', 'is_available', 'created', 'updated']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.kit_code = validated_data.get('kit_code', instance.kit_code)
        instance.name = validated_data.get('name', instance.name)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['history'] = self.get_history(instance)
        return representation

    def get_history(self, obj):
        history_records = obj.history.all()
        serialized_history = []

        for record in history_records:
            changed_by = record.history_user.email if record.history_user else 'Unknown User'

            serialized_record = {
                'change_reason': record.history_type,
                'changed_by': changed_by,
                'timestamp': record.history_date,
                'snapshot': {
                    'id': record.id,
                    'name': record.name,
                    'is_available': record.is_available,
                    'created': record.created,
                    'updated': record.updated,
                }
            }
            serialized_history.append(serialized_record)

        return serialized_history


class UnitModelSerializer(serializers.ModelSerializer):
    unit_kit_name = serializers.SerializerMethodField(read_only=True)
    item_name = serializers.SerializerMethodField(read_only=True)
    item_category_name = serializers.SerializerMethodField(read_only=True)
    unit_kit = serializers.PrimaryKeyRelatedField(
        queryset=Unitkit.objects.all(),
        required=False,
        allow_null=True
    )
    item = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Unit
        fields = ['id', 'item', 'item_name', 'item_category_name', 'serial', 'unit_kit', 'unit_kit_name', 'created', 'updated']

    def get_unit_kit_name(self, obj):
        return obj.unit_kit.name if obj.unit_kit else None
    
    def get_item_name(self, obj):
        return obj.item.name if obj.item else None
    
    def get_item_category_name(self, obj):
        return obj.item.category.name if obj.item else None


    
class KitAssignmentModelSerializer(serializers.ModelSerializer):
    unit_kit = serializers.PrimaryKeyRelatedField(queryset=Unitkit.objects.filter(is_available=True), required=False, allow_null=True)
    unit_kit_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = KitAssignment
        fields = ['id', 'unit_kit', 'assign_to', 'date_assigned', 'date_returned', 'unit_kit_name', 'is_returned', 'remarks']

    def get_unit_kit_name(self, obj):
        return obj.unit_kit.name if obj.unit_kit else None