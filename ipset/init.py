""" Block/admin set init functions module. """
import logging
from ipset.models import AdminAddress


def init_blocked_addrs():
    """ Init blocked addrs on start. """


def init_admin_addrs():
    """ Init admin addrs on start. """
    logging.getLogger('django.server').info(
        'Init deleted %s', AdminAddress.objects.all().delete()
    )
