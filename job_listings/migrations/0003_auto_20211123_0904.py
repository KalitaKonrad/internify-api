# Generated by Django 3.2.8 on 2021-11-23 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job_listings', '0002_auto_20211122_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='job_listings.company'),
        ),
    ]
