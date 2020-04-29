""" Block/admin clean functions module. """
import logging
from datetime import timedelta
from django.utils import timezone
from ipset import libipset
from ipset.models import AdminAddress, setname


ADMIN_ADDR_TIMEOUT = 60


def clean_blocked_addrs():
    """ Clean up old blocked addresses. """


def clean_admin_addrs():
    """ Clean up old admin addresses. """
    timeout = timedelta(minutes=ADMIN_ADDR_TIMEOUT)
    objects = AdminAddress.objects.filter(
        last_access__lt=timezone.now() - timeout,
    )
    for obj in objects:
        libipset.remove_entry(setname(obj.address, 'admin'), obj.address)
    logging.getLogger('django.server').info(
        'Clean deleted %s', objects.delete()
    )
