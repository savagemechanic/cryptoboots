# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import InvestmentPlan, UserProfile, Wallet, UserWallet, PlatformWallet, SuperWallet, WithdrawalRequests, Deposits

# Register your models here.

admin.site.register(InvestmentPlan)
admin.site.register(UserProfile)
admin.site.register(Wallet)
admin.site.register(UserWallet)
admin.site.register(PlatformWallet)
admin.site.register(SuperWallet)
admin.site.register(WithdrawalRequests)
admin.site.register(Deposits)