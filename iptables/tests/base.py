""" Base test class module. """
import logging
from django.test import TestCase, override_settings


@override_settings(IPSETS={})
class IptablesTestCase(TestCase):
    """ Parent class with nice things. """

    def setUp(self):
        """ Init logging and override settings.IPSETS. """
        logging.disable(logging.NOTSET)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def _log(data):
        """ Log the data to the django.server info logger. """
        logging.getLogger('django.server').info(data)
