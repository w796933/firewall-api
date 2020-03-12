""" iptables app URLs module. """
from django.urls import path
from iptables import views


urlpatterns = [
    path('input/accept', views.InputAcceptView.as_view()),
]
