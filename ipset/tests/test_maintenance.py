""" Test module for schedules. """
from django.conf import settings
from ipset.tests.base import IpsetTestCase


class ScheduleTestCase(IpsetTestCase):
    """ Validate ipset task scheduling. """

    def test_middleware(self):
        """ Assert that.... """
        if 'django_q' not in settings.INSTALLED_APPS:
            return
