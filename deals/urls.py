"""startByClick URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from . import views as user_views
from .views import *

urlpatterns = [
    path('',landing,name="landing"),
    path('ideas/',user_views.DealView.as_view(),name= "deals-home"),
    path('idea/<int:id>', deal_details, name='deal-detail'),
    path('idea/new/', DealCreateView.as_view(), name='deal-create'),
    path('idea/<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    path('idea/<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    # path('cabinet/', user_views.cabinet, name="cabinet"),
    # path('idea/<int:pk>/update/', DealUpdateView.as_view(), name='deal-update'),
    # path('idea/<int:pk>/delete/', DealDeleteView.as_view(), name='deal-delete'),
    path('test/',test,name='test'),
    path('myideas/',myideas,name="myideas"),

]
