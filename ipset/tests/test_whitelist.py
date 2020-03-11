""" Whitelist test module. """
from datetime import timedelta
from django.core import mail
from django.utils import timezone
from freezegun import freeze_time
from ipset import libipset
from ipset.tests.base import IpsetTestCase
from ipset.models import WhitelistAddress
from ipset.clean import clean_whitelist, WHITELIST_TIMEOUT
from ipset.init import init_whitelist


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

    def test_exising_ipv4(self):
        """ Test POST of pre-configured IPv4 address. """
        addr = '10.0.0.3'
        if not libipset.test_entry('whitelist4', addr):
            libipset.add_entry('whitelist4', addr)
        response = self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaisesMessage(WhitelistAddress.DoesNotExist, ''):
            WhitelistAddress.objects.get(address=addr)
        libipset.remove_entry('whitelist4', addr)


class WhitelistInitTestCase(IpsetTestCase):
    """ Validate init. """

    def test_init(self):
        """ Test whitelist init. """
        addr = '10.0.0.4'
        if libipset.test_entry('whitelist4', addr):
            libipset.remove_entry('whitelist4', addr)
        self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        WhitelistAddress.objects.get(address=addr)
        init_whitelist()
        with self.assertRaisesMessage(WhitelistAddress.DoesNotExist, ''):
            WhitelistAddress.objects.get(address=addr)
        self.assertTrue(libipset.test_entry('whitelist4', addr))
        libipset.remove_entry('whitelist4', addr)


class WhitelistCleanTestCase(IpsetTestCase):
    """ Validate ipset whitelist clean. """

    def test_freezegun(self):
        """ Test freezegun expired record. """
        elapsed = WHITELIST_TIMEOUT + 5
        freezer = freeze_time(timezone.now() - timedelta(minutes=elapsed))
        freezer.start()
        addr = '10.0.0.5'
        if libipset.test_entry('whitelist4', addr):
            libipset.remove_entry('whitelist4', addr)
        self.client.post(
            '/ipset/whitelist',
            data={'address': addr},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        freezer.stop()

        obj = WhitelistAddress.objects.get(address=addr)
        timeout = timezone.now() + timedelta(minutes=WHITELIST_TIMEOUT)
        self.assertTrue(obj.last_access < timeout)
        libipset.remove_entry('whitelist4', addr)

    def test_clean(self):
        """ Test clean. """

        # Add an expired entry.
        elapsed = WHITELIST_TIMEOUT + 5
        freezer = freeze_time(timezone.now() - timedelta(minutes=elapsed))
        freezer.start()
        addr1 = '10.0.0.6'
        if libipset.test_entry('whitelist4', addr1):
            libipset.remove_entry('whitelist4', addr1)
        self.client.post(
            '/ipset/whitelist',
            data={'address': addr1},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        freezer.stop()

        # Add an unexpired entry.
        elapsed = WHITELIST_TIMEOUT - 5
        freezer = freeze_time(timezone.now() - timedelta(minutes=elapsed))
        freezer.start()
        addr2 = '10.0.0.7'
        if libipset.test_entry('whitelist4', addr2):
            libipset.remove_entry('whitelist4', addr2)
        self.client.post(
            '/ipset/whitelist',
            data={'address': addr2},
            HTTP_X_FORWARDED_HOST='localhost',
        )
        freezer.stop()

        # Clean and test.
        clean_whitelist()
        self.assertFalse(libipset.test_entry('whitelist4', addr1))
        self.assertTrue(libipset.test_entry('whitelist4', addr2))
        libipset.remove_entry('whitelist4', addr2)
