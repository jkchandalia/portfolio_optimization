# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-16 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarginableEquity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarginRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equity', models.CharField(max_length=255)),
                ('strike', models.IntegerField()),
                ('exp_date', models.DateField()),
                ('option_type', models.CharField(max_length=255)),
                ('bid', models.FloatField()),
                ('ask', models.FloatField()),
                ('mark', models.FloatField()),
                ('delta', models.FloatField()),
                ('theta', models.FloatField()),
                ('gamma', models.FloatField()),
                ('vega', models.FloatField()),
                ('equity_price', models.FloatField()),
                ('flavor', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('symbol', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users_who_own', models.ManyToManyField(related_name='owns_options', to='login_app.User')),
            ],
        ),
    ]
