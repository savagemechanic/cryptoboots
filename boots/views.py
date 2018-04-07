# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test

from .decorators import group_required, role_required
from .models import User, UserProfile, Role, InvestmentPlan, Deposits, WithdrawalRequests, PlatformWallet
from .forms import AuthForm, EditProfileForm, WithdrawForm, InvestForm
import constants
from .helpers import login_redirect

# reused vars
platform_wallet = PlatformWallet.objects.get(id=1)
super_wallet = PlatformWallet.objects.get(id=1)
dummy_list_context = {
        'online_bots': 45,
        'offline_bots': 200,
        'total_bots': 245,
        'notifications': [
            'Mike John responded to your email',
            'You have 5 new tasks',
            'You\'re now friend with Andrew',
            'Another Notification',
            'Another One',
        ],
}

# Create your views here.
# AUTH PAGES

def register(request):
    html = 'register.html'
    if request.method == 'GET':
        authform = AuthForm()
        context = {
            'auth_form': authform,
        }
        return render(request, html, context)
    elif request.method == 'POST':
        authform = AuthForm(request.POST)
        if authform.is_valid():
            # get data
            email = authform.cleaned_data['email']
            password = authform.cleaned_data['password']
            try:
                referral = request.GET['referrer']
            except Exception as e:
                referral = None

            # create user and profile...
            user_profile = UserProfile.objects.create_regular_user(email=email,
                password=password,
                referral_code=referral, role_objects=Role.objects)
            user = user_profile.user

            # log user in
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('user_dashboard'))
        # Return an 'invalid login' error message.
        context = {
            'auth_form': authform,
        }
        return render(request, html, context)


def login_view(request):
    html = 'registration/login.html'
    if request.method == 'GET':
        authform = AuthForm()
        context = {
            'auth_form': authform,
        }
        return render(request, html, context)
    elif request.method == 'POST':
        authform = AuthForm(request.POST)
        if authform.is_valid():
            email = authform.cleaned_data['email']
            password = authform.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                next_link = request.POST['next']
                if next_link:
                    return HttpResponseRedirect(next_link)
                return login_redirect(user.userprofile)
        # Return an 'invalid login' error message.
        context = {
            'auth_form': authform,
        }
        return render(request, html, context)


# USER FLUFF PAGES
def index(request):
    html = 'index.html'
    context = {
    }
    return render(request, html, context)

def about_us(request):
    html = 'about_us.html'
    context = {
    }
    return render(request, html, context)

def services(request):
    html = 'services.html'
    context = {
    }
    return render(request, html, context)


# USER PAGES
# @login_required(redirect_field_name='redirect_url', login_url='/login')
# @role_required('regular')
def user_dashboard(request):
    html = 'user_dashboard.html'
    deposits = Deposits.objects.filter(user=request.user.userprofile)
    withdrawals = WithdrawalRequests.objects.filter(user=request.user.userprofile)
    context = {
        'deposits': deposits,
        'withdrawals': withdrawals,
    }
    return render(request, html, context)

# @role_required('regular')
def profile(request):
    html = 'profile.html'
    # if request.user.userprofile.is_superuser:
    #     user_wallet = request.user.userprofile.platformwallet.wallet
    # else:
    userprofile = request.user.userprofile
    if userprofile.is_regular:
        user_wallet = request.user.userprofile.userwallet.wallet
    elif userprofile.is_admin:
        user_wallet = platform_wallet.wallet
    elif userprofile.is_superuser:
        user_wallet = super_wallet.wallet

    if request.method == 'GET':
        editform = EditProfileForm(instance=user_wallet)
        context = {
            'user_wallet': user_wallet,
            'edit_profile_form': editform,
        }
        return render(request, html, context)
    elif request.method == 'POST':
        # to edit user profile
        editform = EditProfileForm(request.POST, instance=user_wallet)
        if editform.is_valid():
            editform.save()
        context = {
            'user_wallet': user_wallet,
            'edit_profile_form': editform,
        }
        return render(request, html, context)

# @role_required('regular')
def wallet(request):
    html = 'wallet.html'
    plans = InvestmentPlan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, html, context)

# @role_required('regular')
def invest_select(request):
    html = 'wallet_invest_select.html'
    plans = InvestmentPlan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, html, context)

# @role_required('regular')
def invest_summary(request, plan_id):
    html = 'wallet_invest_summary.html'
    html_confirm = 'wallet_invest_confirm.html'
    plan = InvestmentPlan.objects.get(id=plan_id)
    form = InvestForm()
    context = {
        'plan': plan,
        'platform_wallet': platform_wallet,
        'coin_types': constants.coin_types,
        'invest_form': form,
    }
    if request.method == 'GET':
        return render(request, html, context)
    elif request.method == 'POST':
        form = InvestForm(request.POST)
        if int(request.POST['amount']) < plan.minimum_deposit:
            form.add_error('amount', 'The deposit amount can\'t be less than the minimum')
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user.userprofile
            deposit.investment_plan = plan
            deposit.save()
            return render(request, html_confirm, context)
        context['invest_form'] = form
        return render(request, html, context)



# @role_required('regular')
def withdraw_confirm(request):
    html = 'wallet_withdraw_confirm.html'
    context = {
    }
    return render(request, html, context)

# @role_required('regular')
def withdraw_form(request):
    if request.method == 'GET':
        html = 'wallet_withdraw_form.html'
        form = WithdrawForm()
        context = {
            'withdraw_form': form,
            'coin_types': constants.coin_types,
        }
        return render(request, html, context)
    elif request.method == 'POST':
        # to edit user profile
        form = WithdrawForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user.userprofile
            withdrawal.save()
            return HttpResponseRedirect(reverse('withdraw_confirm'))
        else:
            context = {
                'withdraw_form': form,
            }
            return render(request, html, context)

def referrals(request):
    html = 'referrals.html'
    plans = InvestmentPlan.objects.all()
    context = {
        'plans': plans,
    }
    return render(request, html, context)


# ADMIN PAGES
# @login_required(redirect_field_name='redirect_url', login_url='/login')
def dashboard_index(request):
    html = 'dashboard.html'
    context = {
        'platformwallet': platform_wallet,
    }
    return render(request, html, context)

def admin_deposits(request):
    html = 'admin_deposits.html'
    pending_deposits = Deposits.objects.filter(status=constants.deposit_status['pending'])
    confirmed_deposits = Deposits.objects.filter(status=constants.deposit_status['completed'])
    context = {
        'platformwallet': platform_wallet,
        'pending_deposits': pending_deposits,
        'confirmed_deposits': confirmed_deposits,
    }
    return render(request, html, context)

def admin_withdrawals(request):
    html = 'admin_withdrawals.html'
    pending_withdrawals = WithdrawalRequests.objects.filter(status=constants.withdrawal_request_status['pending'])
    confirmed_withdrawals = WithdrawalRequests.objects.filter(status=constants.withdrawal_request_status['completed'])
    context = {
        'platformwallet': platform_wallet,
        'pending_withdrawals': pending_withdrawals,
        'confirmed_withdrawals': confirmed_withdrawals,
    }
    return render(request, html, context)

def admin_wallet(request):
    html = 'admin_wallet.html'
    plans = InvestmentPlan.objects.all()
    context = {
        'platformwallet': platform_wallet,
        'plans': plans,
    }
    return render(request, html, context)


# SUPER ADMIN PAGES
# @login_required(redirect_field_name='redirect_url', login_url='/login')
def super_dashboard_index(request):
    html = 'super_dashboard.html'
    all_bots = dummy_list_context['online_bots'] # Query All
    online_bots = dummy_list_context['online_bots'] # Query All Online
    offline_bots = dummy_list_context['online_bots'] # Query All Offline
    # all_bots = list(Bot.objects.all()) # Query All
    # online_bots = list(Bot.objects.filter(active=True)) # Query All Online
    # offline_bots = list(Bot.objects.filter(active= not True)) # Query All Offline
    context = {
        'online_bots': online_bots,
        'offline_bots': offline_bots,
        'total_bots': all_bots,
        'bots': online_bots
    }
    return render(request, html, context)

def super_deposits(request):
    html = 'super_deposits.html'
    all_bots = dummy_list_context['online_bots'] # Query All
    online_bots = dummy_list_context['online_bots'] # Query All Online
    offline_bots = dummy_list_context['online_bots'] # Query All Offline
    context = {
        'online_bots': online_bots,
        'offline_bots': offline_bots,
        'total_bots': all_bots,
        'bots': online_bots
    }
    return render(request, html, context)

def super_withdrawals(request):
    html = 'super_withdrawals.html'
    all_bots = dummy_list_context['online_bots'] # Query All
    online_bots = dummy_list_context['online_bots'] # Query All Online
    offline_bots = dummy_list_context['online_bots'] # Query All Offline
    context = {
        'online_bots': online_bots,
        'offline_bots': offline_bots,
        'total_bots': all_bots,
        'bots': online_bots
    }
    return render(request, html, context)

def super_wallet(request):
    html = 'super_wallet.html'
    all_bots = dummy_list_context['online_bots'] # Query All
    online_bots = dummy_list_context['online_bots'] # Query All Online
    offline_bots = dummy_list_context['online_bots'] # Query All Offline
    context = {
        'online_bots': online_bots,
        'offline_bots': offline_bots,
        'total_bots': all_bots,
        'bots': online_bots
    }
    return render(request, html, context)

def super_users(request):
    html = 'super_users.html'
    all_bots = dummy_list_context['online_bots'] # Query All
    online_bots = dummy_list_context['online_bots'] # Query All Online
    offline_bots = dummy_list_context['online_bots'] # Query All Offline
    context = {
        'online_bots': online_bots,
        'offline_bots': offline_bots,
        'total_bots': all_bots,
        'bots': online_bots
    }
    return render(request, html, context)

# Dashboard handler
# def dashboard_base(request):
#     ''' Render dashboard based on user role '''
#     userprofile = request.user.userprofile
#     # Regular user
#     if userprofile.is_regular:
#         return user_dashboard(request)
#     # Admin
#     elif userprofile.is_admin:
#         return dashboard_index(request)
#     # super user
#     elif userprofile.is_superuser:
#         return super_dashboard_index(request)
#     # anonymous user
#     else:
#         user_passes_test(False, login_url=reverse('login'))

# def bot_detail(request, id):
#     html = 'bot_detail.html'
#     bot = Bot.objects.get(id=id)  # Query By id
#     context = {
#         'bot_name': bot.name,
#         'bot_ip': bot.ip_address,
#         'bot_mac': bot.mac_address,
#         'bot_country': bot.country,
#         'bot_continent': bot.continent,
#         'bot_created_at': bot.created_at,
#         'bot_last_active': bot.last_active,
#         'bot_active': bot.active
#     }
#     return render(request, html, context)
