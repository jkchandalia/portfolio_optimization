# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-17 02:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
        ('portfolio_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='marginableequity',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='margin_available', to='login_app.User'),
        ),
        migrations.AddField(
            model_name='marginrequired',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='margin_required', to='login_app.User'),
        ),
        migrations.AlterField(
            model_name='marginableequity',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='marginrequired',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='option',
            name='users_who_own',
            field=models.ManyToManyField(related_name='options_in_portfolio', to='login_app.User'),
        ),
    ]
