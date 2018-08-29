# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-30 19:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coffeelist', '0002_auto_20180730_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL),
        ),
    ]
