""" Whitelist test module. """
from django.core import mail
from ipset import libipset
from ipset.tests.base import IpsetTestCase
from ipset.models import WhitelistAddress


class WhitelistTestCase(IpsetTestCase):
    """ Validate the ipset whitelist API. """

    def test_no_data(self):
        """ Test POST with no data. """
        response = self.client.post(
            '/ipset/whitelist',
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(mail.outbox) == 1)

    def test_add_invalid(self):
        """ Test POST with a bad address. """
        response = self.client.post(
            '/ipset/whitelist',
            data={'address': 'not-an-ip-address'},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(mail.outbox) == 1)

    def test_add_ipv4(self):
        """ Test POST with IPv4 address. """
        addr = '10.0.0.1'
        if libipset.test_entry('whitelist4', addr):
            libipset.remove_entry('whitelist4', addr)
        response = self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(libipset.test_entry('whitelist4', addr))
        libipset.remove_entry('whitelist4', addr)

    def test_re_add_ipv4(self):
        """ Test re-POST with IPv4 address. """
        addr = '10.0.0.2'
        if libipset.test_entry('whitelist4', addr):
            libipset.remove_entry('whitelist4', addr)
        self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        obj = WhitelistAddress.objects.get(address=addr)
        before = obj.last_access
        response = self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 200)
        obj = WhitelistAddress.objects.get(address=addr)
        self.assertTrue(obj.last_access > before)
        libipset.remove_entry('whitelist4', addr)

    def test_add_ipv6(self):
        """ Test POST with IPv6 address. """


class WhitelistInitTestCase(IpsetTestCase):
    """ Validate ipset whitelist init. """


class WhitelistCleanTestCase(IpsetTestCase):
    """ Validate ipset whitelist clean. """
