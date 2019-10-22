""" Base test class module. """
import random
import string
import subprocess
import logging
from django.test import TestCase, override_settings
from ipset.models import Set


@override_settings(IPSETS={})
class FirewallTestCase(TestCase):
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


class IpsetTestCase(FirewallTestCase):
    """ Parent class with ipset create/destroy methods. """

    setname = None
    setname4 = None
    setname6 = None

    @staticmethod
    def create_set():
        """ Create an ipset and return name and sets created. """
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
        Set.objects.create(name=name)
        name4 = '%s4' % name
        name6 = '%s6' % name
        subprocess.run(
            ['ipset', 'create', name4, 'hash:ip', 'family', 'inet'],
            check=True,
        )
        subprocess.run(
            ['ipset', 'create', name6, 'hash:ip', 'family', 'inet6'],
            check=True,
        )
        return name, name4, name6

    @staticmethod
    def destroy_set(name):
        """ Destroy an ipset. """
        subprocess.run(['ipset', 'destroy', '%s4' % name], check=True)
        subprocess.run(['ipset', 'destroy', '%s6' % name], check=True)

    def setUp(self):
        """ Also create underlying sets before every test. """
        super(IpsetTestCase, self).setUp()
        self.setname, self.setname4, self.setname6 = self.create_set()

    def tearDown(self):
        """ Destroy underlying sets after every test. """
        self.destroy_set(self.setname)


class TwoIpsetTestCase(IpsetTestCase):
    """ Validate set view PUT where there are two sets. """

    setname_b = None
    setname_b4 = None
    setname_b6 = None

    def setUp(self):
        """ Create two underlying sets before every test. """
        super(TwoIpsetTestCase, self).setUp()
        self.setname_b, self.setname_b4, self.setname_b6 = self.create_set()

    def tearDown(self):
        """ Destroy both underlying sets after every test. """
        super(TwoIpsetTestCase, self).tearDown()
        self.destroy_set(self.setname_b)
