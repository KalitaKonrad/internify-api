
from rest_framework import serializers
from .models import Job, Company


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'published',
                  'is_active', 'updated_at', 'slug')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'establishment', 'website_url')
