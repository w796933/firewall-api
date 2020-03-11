""" Blacklist/whitelist init functions module. """
import logging
from ipset.models import WhitelistAddress


def init_blacklist():
    """ Init blacklist on start. """


def init_whitelist():
    """ Init whitelist on start. """
    logging.getLogger('django.server').info(
        'Init deleted %s', WhitelistAddress.objects.all().delete()
    )
