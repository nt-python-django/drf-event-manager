from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import User

phone_validator = RegexValidator(regex=r'^\+998\d{9}$', message='Phone number must be entered in the format: "+998901234567". Equalt to 11 digits allowed.')


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    phone = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('A user with this phone number already exists.')
        return value


    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Passwords do not match.')

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(validators=[phone_validator])

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'bio', 'telegram_id', 'chat_id', 'telegram_username', 'image']
        kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True},
            'image': {'required': False, 'allow_null': True},
        }

    def validate_phone(self, value):
        user = self.instance
        if User.objects.filter(phone=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('A user with this phone number already exists.')
        return value


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError('New passwords do not match.')

        return attrs