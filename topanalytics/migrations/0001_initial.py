# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=254)),
                ('date_added', models.DateTimeField(verbose_name=b'date added')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('entry_date', models.DateTimeField(verbose_name=b'First user entry')),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=254)),
                ('property_id', models.CharField(max_length=254)),
                ('view_id', models.IntegerField(default=0)),
                ('view_name', models.CharField(max_length=254)),
                ('entry_date', models.DateTimeField(verbose_name=b'Website entry date')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='websites',
            field=models.ManyToManyField(blank=True, related_name='users', to='topanalytics.Website'),
        ),
    ]