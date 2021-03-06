# Generated by Django 3.2.8 on 2021-11-29 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_listings', '0014_alter_job_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
    ]
