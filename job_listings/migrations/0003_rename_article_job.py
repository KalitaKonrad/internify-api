# Generated by Django 3.2.8 on 2021-10-21 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_listings', '0002_auto_20211021_1822'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Article',
            new_name='Job',
        ),
    ]
