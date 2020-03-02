""" Base test class module. """
import random
import string
import subprocess
import logging
from django.test import TestCase


class IpsetTestCase(TestCase):
    """ Parent test case class with nice things. """

    def setUp(self):
        """ Init logging. """
        logging.disable(logging.NOTSET)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def _log(data):
        """ Log the data to the django.server info logger. """
        logging.getLogger('django.server').info(data)
