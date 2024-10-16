# Generated by Django 4.1.13 on 2024-09-16 06:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0012_alter_friendship_created_at_alter_likepost_liked_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 16, 12, 0, 34, 650980)),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='liked_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 16, 12, 0, 34, 651979)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 16, 12, 0, 34, 649981)),
        ),
        migrations.AlterField(
            model_name='savepost',
            name='saved_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 9, 16, 12, 0, 34, 650980)),
        ),
    ]
