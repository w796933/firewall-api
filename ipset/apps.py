""" Ipset app config module. """
from django.apps import AppConfig
from django.db.utils import OperationalError


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
        except OperationalError:
            # TODO When the app starts but there aren't yet any migrations.
            pass
        except ValueError as err:
            import logging
            logging.getLogger('django.ipset').error('Sync on ready failed')
            logging.getLogger('django.server').error(str(err))
