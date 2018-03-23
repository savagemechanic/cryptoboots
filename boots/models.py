# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

# Create your models here.

class Role(models.Model):#One-to-One [Each bot has a user]
  name = models.TextField(blank=False, unique=True, max_length=30)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'

class UserProfile(models.Model):#One-to-One [Each bot has a user]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  key = models.TextField(blank=False, unique=True, max_length=150)

  class Meta():
    app_label = 'boots'

class Bot(models.Model):#One-to-One [Each bot has a user]
  name = models.TextField(blank=False, unique=True, max_length=150)
  country = models.TextField( max_length=50, blank=True, null=True)
  continent = models.TextField(max_length=50, blank=True, null=True)
  slug = models.CharField(max_length=50, blank=True, null=True)
  ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, null=True)
  mac_address = models.TextField(max_length=50, blank=True, null=True)
  active = models.NullBooleanField(null=True)
  last_active = models.DateTimeField(blank=True, null=True)
  last_pwd_download = models.DateTimeField(blank=True, null=True)
  listening_port = models.IntegerField(blank=True, null=True)
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'