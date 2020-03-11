""" Blacklist/whitelist clean functions module. """
import logging
from datetime import timedelta
from django.utils import timezone
from ipset import libipset
from ipset.models import WhitelistAddress, setname


WHITELIST_TIMEOUT = 60


def clean_blacklist():
    """ Clean the blacklist. """


def clean_whitelist():
    """ Clean the whitelist. """
    timeout = timedelta(minutes=WHITELIST_TIMEOUT)
    objects = WhitelistAddress.objects.filter(
        last_access__lt=timezone.now() - timeout,
    )
    for obj in objects:
        libipset.remove_entry(setname(obj.address, 'whitelist'), obj.address)
    logging.getLogger('django.server').info(
        'Clean deleted %s', objects.delete()
    )
