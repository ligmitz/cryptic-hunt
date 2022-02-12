"""cryptic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls.conf import include 
from django.contrib import admin
from accounts.views import leaderboard, home, rules, register, activate
from questions.views import Hunt
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = "accounts"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register, name="register"),
    path('leaderboard/',leaderboard, name="leaderboard"),
    path('hunt/',Hunt.as_view(), name='hunt'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name = 'login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'home.html'),name='logout'),
    path('',home, name='home'),
    path('rules/',rules, name="rules"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name="password_reset"), 
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name="password_reset_complete"),
    path('emailVerification/<uidb64>/<token>',activate, name='emailActivate'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),  
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
