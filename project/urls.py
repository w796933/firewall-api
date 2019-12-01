""" Firewall URL config module. """
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = 'Firewall admin'
admin.site.site_title = 'Firewall'
admin.site.site_url = None

urlpatterns = [
    path('ipset/', include('ipset.urls')),
    path('iptables/', include('iptables.urls')),
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
]
