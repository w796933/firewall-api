""" Blacklist test module. """
from django.core import mail
from ipset import libipset
from ipset.tests.base import IpsetTestCase
from ipset.models import BlacklistAddress, BlacklistEvent


class BlacklistTestCase(IpsetTestCase):
    """ Validate the ipset blacklist API. """

    def test_no_data(self):
        """ Test POST with no data. """
        response = self.client.post(
            '/ipset/blacklist',
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(mail.outbox) == 1)

    def test_add_invalid(self):
        """ Test POST with bad data. """

    def test_add_ipv4(self):
        """ Test POST with IPv4 address. """

    def test_re_add_ipv4(self):
        """ Test re-POST with IPv4 address. """

    def test_add_ipv6(self):
        """ Test POST with IPv6 address. """


class BlacklistInitTestCase(IpsetTestCase):
    """ Validate ipset blacklist init. """


class BlacklistCleanTestCase(IpsetTestCase):
    """ Validate ipset blacklist clean. """
