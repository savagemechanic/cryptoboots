# To run:
# python manage.py shell
# import boots.seeders
import os
import sys

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Role, InvestmentPlan, PlatformWallet, Wallet, UserProfile

def seed_all():
    # Roles
    # basic
    regular_role = Role.objects.get_regular_role()
    # admin
    admin_role = Role.objects.get_admin_role()
    # super
    superuser_role = Role.objects.get_super_role()

    # Investment Plans
    bronze = InvestmentPlan.objects.get_or_create(name='Bronze Plan',
        minimum_deposit=10000.00,
        cashout_frequency=14, percent_earning=15,
        referral_commission=1)
    silver = InvestmentPlan.objects.get_or_create(name='Silver Plan',
        description="Popular", minimum_deposit=100000.00,
        cashout_frequency=21, percent_earning=30,
        referral_commission=3)
    gold = InvestmentPlan.objects.get_or_create(name='Gold Plan',
        description="Premium", minimum_deposit=1000000.00,
        cashout_frequency=30, percent_earning=50,
        referral_commission=5)

    # Admins
    admin_user = UserProfile.objects.create_admin(email='admin@gmail.com',
        password='admin', role=admin_role)
    super_user = UserProfile.objects.create_super_user(email='super@gmail.com',
        password='superu', role=superuser_role)

    # Wallets
    wallet = Wallet.objects.get_or_create(eth_address='hfg4849784hrjj4747',
        btc_address="hfg4849784hrjj4747")[0]
    platform_wallet = PlatformWallet.objects.get_or_create(
        wallet=wallet)[0]

seed_all()
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoboots.settings")
    seed_all()