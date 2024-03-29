# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 07:47
from __future__ import unicode_literals

import boots.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boots', '0006_auto_20180406_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveInvestments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invested_amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('status', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', boots.models.AutoDateTimeField(default=django.utils.timezone.now, editable=False)),
                ('investment_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boots.InvestmentPlan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boots.UserProfile')),
            ],
        ),
    ]
