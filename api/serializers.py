from rest_framework import serializers
from stuffs.models import Unit, Unitkit, Category, UnitStatus
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
        fields = ['id', 'first_name', 'last_name', 'email', 'position', 'contact', 'birth_date', 'is_staff', 'employee_id', 'is_active', 'department']

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
    assign_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    kit_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Unitkit
        fields = ['id', 'name', 'kit_code', 'assign_to', 'history', 'created', 'updated']
    
    def validate(self, data):
        if 'kit_code' not in data or not data['kit_code']:
            data['kit_code'] = str(uuid.uuid4()).replace("-", "").upper()[:8]
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        assign_to_data = validated_data.pop('assign_to', None)
        
        # Update simple fields directly on the instance
        instance.kit_code = validated_data.get('kit_code', instance.kit_code)
        instance.name = validated_data.get('name', instance.name)
        
        # Update assign_to field if provided
        if assign_to_data:
            instance.assign_to = assign_to_data
        
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
                    'created': record.created,
                    'updated': record.updated,
                }
            }
            serialized_history.append(serialized_record)

        return serialized_history

class UnitModelSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    item_status = serializers.PrimaryKeyRelatedField(queryset=UnitStatus.objects.all(), required=False, allow_null=True)
    create_by = UserModelSerializer(read_only=True)
    unit_kit = serializers.PrimaryKeyRelatedField(queryset=Unitkit.objects.all(), required=False, allow_null=True)
    history = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ['id', 'barcode', 'create_by', 'name', 'category', 'item_status', 'model', 'date_purchased', 'cost', 'serial', 'unit_kit', 'history', 'created', 'updated']

    def update(self, instance, validated_data):
        # Handle updating simple fields directly on the instance
        instance.name = validated_data.get('name', instance.name)
        instance.model = validated_data.get('model', instance.model)
        instance.date_purchased = validated_data.get('date_purchased', instance.date_purchased)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.serial = validated_data.get('serial', instance.serial)
        
        # Handle updating nested relationships (e.g., category, item_status, unit_kit)
        category_data = validated_data.pop('category', None)
        if category_data:
            instance.category = category_data
        else:
            instance.category = None

        item_status_data = validated_data.pop('item_status', None)
        if item_status_data:
            instance.item_status = item_status_data
        else:
            instance.item_status = None
        
        unit_kit_data = validated_data.pop('unit_kit', None)
        if unit_kit_data:
            instance.unit_kit = unit_kit_data
        else:
            instance.unit_kit = None
        
        instance.save()
        return instance

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
                    'category': record.category.name if record.category else None,
                    'item_status': record.item_status.name if record.item_status else None,
                    'model': record.model,
                    'date_purchased': record.date_purchased,
                    'cost': record.cost,
                    'serial': record.serial,
                    'unit_kit': record.unit_kit.id if record.unit_kit else None,
                    'created': record.created,
                    'updated': record.updated,
                }
            }
            serialized_history.append(serialized_record)

        return serialized_history
