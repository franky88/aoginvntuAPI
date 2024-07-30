from rest_framework import serializers
from stuffs.models import Unit, Unitkit, Category, User, UnitStatus, Profile, Department
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
import uuid

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenVerifySerializer(TokenVerifySerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class MyTokenVerifyView(TokenVerifyView):
    serializer_class = MyTokenVerifySerializer

class DepartmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class ProfileModelSerializer(serializers.ModelSerializer):
    department = DepartmentModelSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'employee_id', 'contact', 'department']

class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'profile']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = f"{instance.first_name} {instance.last_name}"
        if hasattr(instance, 'profile') and instance.profile:
            representation['department'] = (instance.profile.department.name if instance.profile.department else None)
        else:
            representation['department'] = None
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
            changed_by = record.history_user.username if record.history_user else 'Unknown User'

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
        fields = ['id', 'create_by', 'name', 'category', 'item_status', 'model', 'date_purchased', 'cost', 'serials', 'unit_kit', 'history', 'created', 'updated']

    def update(self, instance, validated_data):
        # Handle updating simple fields directly on the instance
        instance.name = validated_data.get('name', instance.name)
        instance.model = validated_data.get('model', instance.model)
        instance.date_purchased = validated_data.get('date_purchased', instance.date_purchased)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.serials = validated_data.get('serials', instance.serials)
        
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
            changed_by = record.history_user.username if record.history_user else 'Unknown User'

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
                    'serials': record.serials,
                    'unit_kit': record.unit_kit.id if record.unit_kit else None,
                    'created': record.created,
                    'updated': record.updated,
                }
            }
            serialized_history.append(serialized_record)

        return serialized_history
