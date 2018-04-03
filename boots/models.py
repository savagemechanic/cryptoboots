# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from constants import withdrawal_request_status, deposit_status

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

# Create your models here.

class InvestmentPlan(models.Model):
  name = models.TextField(blank=False, unique=True, max_length=150)
  description = models.TextField(max_length=350, blank=True, null=True)
  minimum_deposit = models.DecimalField(max_digits=19, decimal_places=2)
  cashout_frequency = models.IntegerField(blank=True, null=True) # number of days
  percent_earning = models.DecimalField(max_digits=5, decimal_places=2) # %
  referral_commission = models.DecimalField(max_digits=5, decimal_places=2) # % commission for referrals
  instant_withdrawal = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class UserProfile(models.Model):#One-to-One [Each bot has a user]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  referral_code = models.CharField(blank=False, unique=True, max_length=50)
  referrer = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True) # user that referred this user
  investment_plans = models.ManyToManyField(InvestmentPlan)
  payee_type = models.IntegerField(blank=True, null=True)

  class Meta():
    app_label = 'boots'
    permissions = (('can_view_user_dashboard', 'To view user dashboard'),
    ('can_view_admin_dashboard', 'To view admin dashboard'),
    ('can_view_super_admin_dashboard', 'To view super admin dashboard'))


class Wallet(models.Model):#One-to-One [Each bot has a user]
  balance = models.DecimalField(max_digits=19, decimal_places=2)
  eth_address = models.TextField( max_length=250, blank=True, null=True)
  btc_address = models.TextField(max_length=250, blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class UserWallet(models.Model):#One-to-One [Each bot has a user]
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  # currency = models.CharField(max_length=10, default='USD')
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  last_withdrawal = models.DateTimeField(blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class WithdrawalRequests(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=19, decimal_places=2)
  status = models.IntegerField(default=withdrawal_request_status['pending'])
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class Deposits(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=19, decimal_places=2)
  status = models.IntegerField(default=deposit_status['pending'])
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class PlatformWallet(models.Model):
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  last_payout = models.DateTimeField(blank=True, null=True) # last time user was paid from wallet
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class SuperWallet(models.Model):
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  last_payout = models.DateTimeField(blank=True, null=True) # last time user was paid from wallet
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'