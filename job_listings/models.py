from django.db import models
from django.utils import timezone
# Create your models here.
from users.models import User
from django.utils.text import slugify
from django.db.models import Max


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    establishment = models.DateTimeField(blank=True, null=True)
    website_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(to=User, on_delete=models.CASCADE)

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
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    slug = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        ordering = ('-published',)

    objects = models.Manager()  # default manager
    jobobjects = JobObjects()  # custom manager - shows only active jobs

    def __str__(self):
        return self.title

    def on_create(self, *args, **kwargs):
        print(args)
        print(kwargs)
        last_id = Job.objects.all().aggregate(Max('id'))['id__max'] or 0

        self.slug = slugify(self.title) + '-' + str(last_id + 1)

    def save(self, *args, **kwargs):
        # if there is not self.pk then the object hasn't been created yet
        if not self.pk:
            self.on_create(*args, **kwargs)

        return super().save(*args, **kwargs)
