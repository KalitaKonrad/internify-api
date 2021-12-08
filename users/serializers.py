from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from job_listings.models import Company
from job_listings.serializers import UserSerializer
from .models import Employee
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=60, min_length=8, write_only=True)
    user_type = serializers.CharField(
        max_length=15, min_length=5, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'user_type']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        user_type = attrs.get('user_type', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username should only contain alphanumeric characters')

        if user_type not in ['is_company', 'is_employee']:
            raise serializers.ValidationError(
                'Wrong user type')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=1)
    password = serializers.CharField(
        max_length=50, min_length=1, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    user_type = serializers.CharField(max_length=255, read_only=True)

    tokens = serializers.CharField(
        max_length=255, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens', 'user_type']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'user_type': 'is_company' if user.is_company == True else 'is_employee',
            'tokens': user.tokens
        }


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    # write_only = True -> we don't send the password back (fixes security issue)
    password = serializers.CharField(
        min_length=8, max_length=50, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset token is invalid', 401)

            user.set_password(password)
            user.save()
            return user

        except Exception as e:

            raise AuthenticationFailed('The reset token is invalid', 401)


class UserCompanyTypeSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'slug', 'owner',)  # 'photo'


class UserEmployeeTypeSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'user')  # 'photo'

