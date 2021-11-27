
from rest_framework import serializers
from .models import Job, Company
from users.models import User


class JobSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'published',
                  'is_active', 'updated_at', 'slug')
        read_only_fields = ['slug']



class UserSerializer(serializers.ModelSerializer):
    # photo = serializers.URLField(source='get_photo_url')

    class Meta:
        model = User
        fields = ('id', 'username', 'email')  # 'photo'


class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, required=False)  # var name has to be the same as string in fields

    class Meta:
        model = Company
        fields = ('id', 'name', 'establishment', 'website_url', 'owner')
        read_only_fields = ['owner']
