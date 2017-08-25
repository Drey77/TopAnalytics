# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 08:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topanalytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='websites',
        ),
        migrations.AddField(
            model_name='website',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='websites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tag',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date added'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='label',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='website',
            name='account_id',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='website',
            name='entry_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'Website entry date'),
        ),
        migrations.AlterField(
            model_name='website',
            name='property_id',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='website',
            name='view_id',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='website',
            name='view_name',
            field=models.CharField(blank=True, max_length=254),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]