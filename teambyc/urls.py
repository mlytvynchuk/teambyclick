"""teambyc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static

from django.urls import path,include
from django.conf import settings

from users import views as user_views
from django.contrib.auth import views as auth_views

from django.conf.urls.i18n import i18n_patterns
from deals import views as d_views

urlpatterns = [
    path('admin/', admin.site.urls),

# urlpatterns += i18n_patterns(
    path('', include('deals.urls')),
    path('',include('users.urls')),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
         template_name='users/password-reset.html'),
         name='password_reset'
         ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='users/password-reset-done.html'),
         name='password_reset_done'
         ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='users/password-reset-confirm.html'),
         name='password_reset_confirm'
         ),
path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='users/password-reset-complete.html'),
         name='password_reset_complete'
         ),
    path('profile/', user_views.profile, name='profile'),
    path('people/', user_views.people, name='people'),
    path('people/<str:slug>', user_views.userDetails, name='user-details'),
    path('ajax/load-cities/', d_views.load_cities, name='ajax_load_cities'),
    path('ajax/load-cities-users/', user_views.load_cities, name='ajax_load_cities_users'),
    path('i18n/', include('django.conf.urls.i18n')),
    # prefix_default_language=False,
]\
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
