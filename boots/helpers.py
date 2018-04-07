
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


def login_redirect(user_profile):
    ''' Redirect to page based on role '''
    # Regular user
    if user_profile.is_regular:
        return HttpResponseRedirect(reverse('user_dashboard'))
    # Admin
    elif user_profile.is_admin:
        return HttpResponseRedirect(reverse('dashboard_index'))
    # super user
    elif user_profile.is_superuser:
        return HttpResponseRedirect(reverse('super_dashboard_index'))