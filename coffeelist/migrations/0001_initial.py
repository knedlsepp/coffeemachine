# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-30 19:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('date',
                 models.DateTimeField(verbose_name='Date of transaction')),
                ('euros', models.DecimalField(decimal_places=2, max_digits=6)),
                ('person',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('date',
                 models.DateTimeField(
                     verbose_name='Date when the price changed')),
                ('euros',
                 models.DecimalField(
                     decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('date',
                 models.DateTimeField(verbose_name='date of purchase')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('tag_value', models.CharField(max_length=200, unique=True)),
                ('owner',
                 models.ForeignKey(
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='tag',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='coffeelist.Tag'),
        ),
    ]
