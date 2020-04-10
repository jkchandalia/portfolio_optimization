# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-17 02:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0002_auto_20191117_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marginableequity',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='margin_available', to='login_app.User'),
        ),
        migrations.AlterField(
            model_name='marginrequired',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='margin_required', to='login_app.User'),
        ),
    ]