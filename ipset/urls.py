""" IP set URLs module. """
from django.urls import path
from ipset import views


urlpatterns = [
    path('admin', views.AdminView.as_view()),
    path('block', views.BlockView.as_view()),
]
