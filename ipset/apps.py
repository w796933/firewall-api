""" Ipset apps module. """
import sys
from django.apps import AppConfig


class IpsetConfig(AppConfig):
    """ Ipset app config. """
    name = 'ipset'
    verbose_name = 'IP set'

    def ready(self):
        """ Run init when the app starts as an ASGI application. """
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from ipset.init import init_blocked_addrs, init_admin_addrs

            init_blocked_addrs()
            init_admin_addrs()
