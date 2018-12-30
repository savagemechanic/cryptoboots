from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    # user fluff pages
    url(r'^$', views.index, name='index'),
    url(r'^about_us', views.about_us, name='about_us'),
    url(r'^services', views.services, name='services'),

    # user pages
    url(r'^dashboard', views.user_dashboard, name='user_dashboard'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^wallet$', views.wallet, name='wallet'),
    url(r'^wallet/withdraw$', views.withdraw_form, name='withdraw_form'),
    url(r'^wallet/withdraw/confirm', views.withdraw_confirm, name='withdraw_confirm'),
    url(r'^wallet/invest$', views.invest_select, name='invest'),
    url(r'^wallet/invest/summary/(?P<plan_id>[0-9]+)$', views.invest_summary, name='invest_summary'),
    url(r'^referrals', views.referrals, name='referrals'),

    # admin pages
    url(r'^admin/home', views.dashboard_index, name='dashboard_index'),
    url(r'^admin/deposits$', views.admin_deposits, name='admin_deposits'),
    url(r'^admin/deposits/(?P<deposit_id>[0-9]+)$', views.admin_deposit_detail, name='admin_deposit_detail'),
    url(r'^admin/deposits/(?P<deposit_id>[0-9]+)/confirm$', views.admin_confirm_deposit, name='admin_confirm_deposit'),
    url(r'^admin/withdrawals$', views.admin_withdrawals, name='admin_withdrawals'),
    url(r'^admin/withdrawals/(?P<withdrawal_id>[0-9]+)$', views.admin_withdrawal_detail, name='admin_withdrawal_detail'),
    url(r'^admin/withdrawals/(?P<withdrawal_id>[0-9]+)/confirm$', views.admin_confirm_withdrawal, name='admin_confirm_withdrawal'),
    url(r'^admin/wallet', views.admin_wallet, name='admin_wallet'),

    # super admin
    url(r'^super_admin/home', views.super_dashboard_index, name='super_dashboard_index'),
    url(r'^super_admin/deposits', views.super_deposits, name='super_deposits'),
    url(r'^super_admin/withdrawals', views.super_withdrawals, name='super_withdrawals'),
    url(r'^super_admin/wallet', views.super_wallet, name='super_wallet'),
    url(r'^super_admin/users', views.super_users, name='super_users'),

    # auth management pages
    url(r'^register', views.register, name='register'),
    # url(r'^login', views.login, name='login'),
    url(r'^accounts/', include('django.contrib.auth.urls'), name='accounts'),
    url(r'^login', views.login_view, name='login'),
    # url(r'^bots/online', views.online_bots, name='online_bots'),
    # url(r'^bots/offline', views.offline_bots, name='offline_bots'),
    # url(r'^bots/(?P<id>[0-9]{1})/', views.bot_detail, name='bot_detail'),
]