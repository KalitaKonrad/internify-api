
from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'title', 'description', 'published',
                  'is_active', 'updated_at', 'slug')
