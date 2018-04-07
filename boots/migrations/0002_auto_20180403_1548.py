# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-03 15:48
from __future__ import unicode_literals

import boots.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', boots.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='boots.Role'),
            preserve_default=False,
        ),
    ]