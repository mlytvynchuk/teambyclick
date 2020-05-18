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
from django.urls import path, include
from . import views as user_views
from .views import *

urlpatterns = [
    path("", landing, name="landing"),
    path("projects/", user_views.DealView.as_view(), name="deals-home"),
    # path("ideas/", user_views.DealView.as_view(), name="ideas-home"),
    path("projects/<int:id>", deal_details, name="deal-detail"),
    path("projects/new/", DealCreateView.as_view(), name="deal-create"),
    path("projects/<int:pk>/update/", DealUpdateView.as_view(), name="deal-update"),
    path("projects/<int:pk>/delete/", DealDeleteView.as_view(), name="deal-delete"),
    path("myprojects/", myideas, name="myideas"),
    path("projects/<int:id>/like/", like_deal, name="deal-like"),
]
