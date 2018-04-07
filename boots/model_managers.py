
from django.db import models
from django.contrib.auth.models import User

class RoleManager(models.Manager):
    def get_admin_role(self):
        return self.get_or_create(name='admin')[0]

    def get_super_role(self):
        return self.get_or_create(name='superuser')[0]

    def get_regular_role(self):
        return self.get_or_create(name='regular')[0]


class UserProfileManager(models.Manager):
    def create_user_with_role(self, email, password, role=None,
        use_referral_code=False):
        # create user
        user = User.objects.create_user(email=email,
                username=email,
                password=password)
        # create user profile
        if use_referral_code:
            user_profile = self.create(user=user, role=role, referral_code=email)
        else:
            user_profile = self.create(user=user, role=role)
        return user_profile

    def create_admin(self, email, password, role=None, role_objects=None):
        if not role:
            admin_role = role_objects.get_admin_role()
        else:
            admin_role = role

        # create user and profile
        return self.create_user_with_role(email=email,
            password=password, role=admin_role, use_referral_code=True)
    
    def create_super_user(self, email, password, role=None, role_objects=None):
        if not role:
            super_role = role_objects.get_super_role()
        else:
            super_role = role

        # create user and profile
        return self.create_user_with_role(email=email,
            password=password, role=super_role, use_referral_code=True)
    
    def create_regular_user(self, email, password, role=None, referral_code=None, role_objects=None):
        ''' Create a basic user with the referrer and wallet and 
        generate referral code
        @returns: UserProfile object '''
        # get or create regular role
        if not role:
            user_role = role_objects.get_regular_role()
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

    def get_users_by_role(self, role):
        return self.filter(role=role)
