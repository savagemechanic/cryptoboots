# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
    context = {
    }
    return render(request, html, context)

def register_user(request):
    html = 'register.html'
    context = {
    }
    return render(request, html, context)

def authenticate_user(request):
    from django.contrib.auth import authenticate
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        redirect(to='/app/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse('Invalid Credentials', status=401)


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
def user_dashboard(request):
    html = 'user_dashboard.html'
    context = {
    }
    return render(request, html, context)

def profile(request):
    html = 'profile.html'
    context = {
    }
    return render(request, html, context)

def wallet(request):
    html = 'wallet.html'
    context = {
    }
    return render(request, html, context)

def referrals(request):
    html = 'referrals.html'
    context = {
    }
    return render(request, html, context)


# ADMIN PAGES
# @login_required(redirect_field_name='redirect_url', login_url='/login')
def dashboard_index(request):
    html = 'dashboard.html'
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

def admin_deposits(request):
    html = 'admin_deposits.html'
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

def admin_withdrawals(request):
    html = 'admin_withdrawals.html'
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

def admin_wallet(request):
    html = 'admin_wallet.html'
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