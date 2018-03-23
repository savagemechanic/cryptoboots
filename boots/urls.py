from django.conf.urls import url, include
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us', views.about_us, name='about_us'),
    url(r'^services', views.services, name='services'),
    url(r'^admin', views.dashboard_index, name='dashboard_index'),
    url(r'^register', views.register, name='register'),
    # url(r'^login', views.login, name='login'),
    url(r'^accounts/', include('django.contrib.auth.urls'), name='login'),
    # url(r'^login_user', views.authenticate_user, name='authenticate'),
    # url(r'^bots/online', views.online_bots, name='online_bots'),
    # url(r'^bots/offline', views.offline_bots, name='offline_bots'),
    # url(r'^bots/(?P<id>[0-9]{1})/', views.bot_detail, name='bot_detail'),
]