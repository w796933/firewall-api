""" IP set URLs module. """
from django.urls import path
from ipset import views


urlpatterns = [
    path('entry/', views.EntryView.as_view()),
    path('set/', views.SetView.as_view()),
]
