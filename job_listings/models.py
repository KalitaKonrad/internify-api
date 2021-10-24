from django.db import models
from django.utils import timezone
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    establishment = models.DateTimeField(blank=True)
    website_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-establishment',)

    def __str__(self):
        return self.name


class Job(models.Model):

    class JobObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_active=True)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    published = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE)

    slug = models.SlugField(max_length=250, unique_for_date='published')

    class Meta:
        ordering = ('-published',)

    objects = models.Manager()  # default manager
    jobobjects = JobObjects()  # custom manager - shows only active jobs

    def __str__(self):
        return self.title
