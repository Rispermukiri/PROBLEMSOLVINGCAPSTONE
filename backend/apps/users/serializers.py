"""
Users serializers for AttachLink.
Handles registration, login token payloads, and user response serialization.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serialize core user information."""

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'is_active',
            'email_verified',
            'created_at',
        ]
        read_only_fields = ['id', 'is_active', 'email_verified', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Validate and create new student/employer users."""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'role']

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_role(self, value):
        allowed_roles = ['student', 'employer']
        if value not in allowed_roles:
            raise serializers.ValidationError('Role must be either student or employer.')
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords must match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customize JWT payload to include user profile data."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        token['is_active'] = user.is_active
        token['email_verified'] = user.email_verified
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data
