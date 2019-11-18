""" Ipset app config module. """
from django.apps import AppConfig


class IpsetConfig(AppConfig):
    """ App config class. """

    name = 'ipset'
    verbose_name = 'IP set'

    def ready(self):
        """ Sync and clean IP sets when the project is ready. Send
        admin email on failure. """
        from ipset.maintenance import sync

        try:
            sync()
        except ValueError as err:
            import logging
            logging.getLogger('django.ipset').error(str(err))
            logging.getLogger('django.server').error(str(err))
