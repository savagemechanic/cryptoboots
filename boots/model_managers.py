
from django.db import models
from .models import User

class RoleManager(models.Manager):
    def get_admin():
        return self.get_or_create('admin')[0]

    def get_super_user():
        return self.get_or_create('superuser')[0]

    def get_regular_user():
        return self.get_or_create('regular')[0]


class UserProfileManager(models.Manager):
    def create_user_with_role(email, password, role=None):
        # create user
        user = User.objects.create_user(email=email,
                username=email,
                password=password)
        # create user profile
        user_profile = self.create(user=user, role=role)
        return user_profile

    def create_admin(email, password, role=None):
        if not role:
            admin_role = Role.objects.get_admin()
        else:
            admin_role = role

        # create user and profile
        return self.create_user_with_role(email=email,
            password=password, role=admin_role)
    
    def create_super_user(email, password, role=None):
        if not role:
            super_role = Role.objects.get_super_user()
        else:
            super_role = role

        # create user and profile
        return self.create_user_with_role(email=email,
            password=password, role=super_role)
    
    def create_regular_user(email, password, role=None, referral_code=None):
        ''' Create a basic user with the referrer and wallet and 
        generate referral code
        @returns: UserProfile object '''
        # get or create regular role
        if not role:
            user_role = Role.objects.get_regular_user()
        else:
            user_role = role

        # create user and profile
        user_profile = self.create_user_with_role(email=email,
            password=password, role=user_role)
        
        # get and set user's referrer if exists
        referring_user = None
        if referral_code:
            try:
                referring_user = self.get(referral_code=referral_code)
            except Exception as e:
                pass
        
        # generate user referral_code
        user_profile.referral_code = user_profile.generate_referral_code(
            email, user_profile.id)
        user_profile.referrer = referring_user
        user_profile.save()
        # create wallet for user
        user_profile.create_wallet()

        return user_profile
