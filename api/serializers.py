from rest_framework import serializers
from stuffs.models import Unit, Unitkit, Category, UnitStatus, KitAssignment
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
        fields = ['id', 'first_name', 'last_name', 'email', 'position', 'contact', 'birth_date', 'is_superuser', 'is_staff', 'employee_id', 'is_active', 'is_working', 'department', 'last_login']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = f"{instance.first_name} {instance.last_name}"
        return representation

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class UnitStatusModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitStatus
        fields = ['id', 'name']

class UnitKitModelSerializer(serializers.ModelSerializer):
    kit_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Unitkit
        fields = ['id', 'name', 'kit_code', 'history', 'is_available', 'created', 'updated']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update simple fields directly on the instance
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
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    item_status = serializers.PrimaryKeyRelatedField(queryset=UnitStatus.objects.all(), required=False, allow_null=True)
    create_by = UserModelSerializer(read_only=True)
    unit_kit = serializers.PrimaryKeyRelatedField(queryset=Unitkit.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Unit
        fields = ['id', 'barcode', 'create_by', 'name', 'descriptions', 'category', 'item_status', 'model', 'date_purchased', 'cost', 'serial', 'unit_kit', 'created', 'updated']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.category:
    #         representation['category'] = instance.category.name
        
    #     return representation
    
class KitAssignmentModelSerializer(serializers.ModelSerializer):
    unit_kit = serializers.PrimaryKeyRelatedField(queryset=Unitkit.objects.filter(is_available=True), required=False, allow_null=True)

    class Meta:
        model = KitAssignment
        fields = ['id', 'unit_kit', 'assign_to', 'date_assigned', 'date_returned', 'is_returned', 'is_returned', 'remarks', 'history']
    
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
                    'unit_kit': record.unit_kit.name,
                    'assign_to': record.assign_to,
                    'date_assigned': record.date_assigned,
                    'date_returned': record.date_returned,
                    'is_available': record.is_available,
                    'is_returned': record.is_returned,
                    'remarks': record.remarks,
                    'updated': record.updated,
                }
            }
            serialized_history.append(serialized_record)

        return serialized_history