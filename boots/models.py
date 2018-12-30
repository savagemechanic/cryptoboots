# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from constants import withdrawal_request_status, deposit_status, coin_types, investment_status
from .model_managers import RoleManager, UserProfileManager
# helpers
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

def get_matching_key(value, collection, upper=False):
    for key in collection:
      if value == collection[key]:
        if upper:
          return key.upper()
        else:
          return key
    return None

def get_coin_type_name(coin_type):
    return get_matching_key(coin_type, coin_types, upper=True)

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


class Role(models.Model):
  name = models.CharField(blank=False, unique=True, max_length=50)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)
  objects = RoleManager()

  class Meta():
    app_label = 'boots'


class Wallet(models.Model):#One-to-One [Each bot has a user]
  balance = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
  eth_address = models.TextField(max_length=250, blank=True, null=True)
  btc_address = models.TextField(max_length=250, blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class UserWallet(models.Model):#One-to-One [Each bot has a user]
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
  # currency = models.CharField(max_length=10, default='USD')
  user = models.OneToOneField('UserProfile', on_delete=models.CASCADE)
  last_withdrawal = models.DateTimeField(blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  class Meta():
    app_label = 'boots'


class UserProfile(models.Model):#One-to-One [Each bot has a user]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  referral_code = models.CharField(blank=False, unique=True, max_length=50)
  referrer = models.ForeignKey('UserProfile', on_delete=models.CASCADE, null=True) # user that referred this user
  investment_plans = models.ManyToManyField(InvestmentPlan)
  payee_type = models.IntegerField(blank=True, null=True)
  objects = UserProfileManager()

  def generate_referral_code(self, email, user_id):
    return email.split('@')[0] + str(user_id)

  def create_wallet(self):
    ''' Create wallet for user '''
    # create wallet
    wallet = Wallet()
    wallet.save()
    # create user wallet
    user_wallet = UserWallet(wallet=wallet, user=self)
    user_wallet.save()

  @property
  def is_regular(self):
    return self.role.name == 'regular'

  @property
  def is_admin(self):
    return self.role.name == 'admin'

  @property
  def is_superuser(self):
    return self.role.name == 'superuser'

  @property
  def regular_user_count(self):
    reg_users = UserProfile.objects.get_users_by_role(role=Role.objects.get_regular_role())
    return len(reg_users)

  class Meta():
    app_label = 'boots'
    permissions = (('can_view_user_dashboard', 'To view user dashboard'),
    ('can_view_admin_dashboard', 'To view admin dashboard'),
    ('can_view_super_admin_dashboard', 'To view super admin dashboard'))


class ActiveInvestments(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
  invested_amount = models.DecimalField(max_digits=19, decimal_places=2, blank=False, null=False)
  status = models.IntegerField(default=investment_status['active'])
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  @property
  def days_taken(self):
    ''' Days used up on plan '''
    days_taken = datetime.datetime(self.created_at) - datetime.datetime.now()
    return days_taken.days()

  @property
  def days_left(self):
    ''' Days left to cashout '''
    days_left = self.investment_plan.cashout_frequency - self.days_taken
    return days_left

  @property
  def profit(self):
    ''' Amount gained since plan activation *** '''
    days_left = self.investment_plan.cashout_frequency - self.days_taken
    return days_left


class WithdrawalRequests(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=19, decimal_places=2, blank=False, null=False)
  coin_type = models.IntegerField(default=coin_types['btc'], blank=False, null=False)
  address = models.TextField(max_length=250, blank=False, null=False)
  status = models.IntegerField(default=withdrawal_request_status['pending'])
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  @property
  def coin_type_name(self):
    return get_coin_type_name(self.coin_type)

  @property
  def status_name(self):
    return get_matching_key(self.status, withdrawal_request_status, upper=True)

  @property
  def is_confirmed(self):
    return self.status == withdrawal_request_status['completed']

  @property
  def is_pending(self):
    return self.status == withdrawal_request_status['pending']

  class Meta():
    app_label = 'boots'


class Deposits(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=19, decimal_places=2, blank=False, null=False)
  coin_type = models.IntegerField(default=coin_types['btc'], blank=False, null=False)
  sender_address = models.TextField(max_length=250, blank=False, null=False)
  recipient_address = models.TextField(max_length=250, blank=False, null=False)
  investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE)
  status = models.IntegerField(default=deposit_status['pending'])
  created_at = models.DateTimeField(default=timezone.now, editable=False)
  updated_at = AutoDateTimeField(default=timezone.now, editable=False)

  @property
  def coin_type_name(self):
    return get_coin_type_name(self.coin_type)

  @property
  def status_name(self):
    return get_matching_key(self.status, deposit_status, upper=True)

  @property
  def is_confirmed(self):
    return self.status == deposit_status['completed']

  @property
  def is_pending(self):
    return self.status == deposit_status['pending']

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