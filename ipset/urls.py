""" IP set URLs module. """
from django.urls import path
from ipset import views


urlpatterns = [
    path('blacklist', views.BlacklistView.as_view()),
    path('whitelist', views.WhitelistView.as_view()),
]
