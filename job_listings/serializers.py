
from rest_framework import serializers
from .models import Job, Company
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # photo = serializers.URLField(source='get_photo_url')

    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # 'photo'


class CompanySerializer(serializers.ModelSerializer):
    # var name has to be the same as string in fields
    slug = serializers.SlugField(required=False, read_only=True)
    owner = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Company
        fields = ('id', 'name', 'establishment',
                  'website_url', 'owner', 'slug', 'headquarters', 'size')
        read_only_fields = ['owner']


class JobSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)
    company = CompanySerializer(read_only=True, required=False)

    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'published',
                  'is_active', 'updated_at', 'slug', 'company',
                  'salary_min', 'salary_max', 'is_remote', 'experience')
        read_only_fields = ['slug', 'company']
