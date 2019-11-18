""" Test module for EntryView PUT. """
from django.core import mail
from ipset.models import Entry
from ipset.tests.base import IpsetTestCase
from ipset import libipset


class EntryViewPutTestCase(IpsetTestCase):
    """ Validate entry view PUT. """

    def test_advance_expires(self):
        """ Assert expiry advances on re-PUT. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            old_expiry = entry.expires

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(old_expiry < entry.expires)

    def test_bad_address(self):
        """ Assert 400 on bad address. """
        response = self.client.put(
            '/ipset/entry/',
            content_type='application/json',
            data={'entry': 'snork', 'address': 'snork'},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.context['exception_value'], 'Bad address')
        self.assertTrue('Bad address' in mail.outbox[0].subject)

    def test_update_ipv4_address(self):
        """ Assert expiry replaces address and advances expiry on re-PUT. """
        addr1 = '10.10.10.10'
        addr2 = '10.10.10.20'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr1},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr1)
            old_expiry = entry.expires

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr2},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr2)
            self.assertTrue(old_expiry < entry.expires)

    def test_update_ipv6_address(self):
        """ Assert expiry replaces address and advances expiry on re-PUT. """
        addr1 = 'fda3:9214:f305:abf7::1'
        addr2 = 'fda3:9214:f305:abf7::2'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr1},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr1)
            old_expiry = entry.expires

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr2},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr2)
            self.assertTrue(old_expiry < entry.expires)

    def test_update_ipv4_to_ipv6_address(self):
        """ Assert expiry replaces address and advances expiry on re-PUT. """
        addr1 = '10.10.10.10'
        addr2 = 'fda3:9214:f305:abf7::2'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr1},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr1)
            old_expiry = entry.expires

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr2},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.address == addr2)
            self.assertTrue(old_expiry < entry.expires)


class EntryViewPutMembershipTestCase(IpsetTestCase):
    """ Validate ipset membership for entry view PUT. """

    def test_update_ipv4_to_ipv6_address(self):
        """ Assert expiry replaces address and advances expiry on re-PUT. """
        addr1 = '10.10.10.10'
        addr2 = 'fda3:9214:f305:abf7::2'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr1},
            )
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            self.assertTrue(addr1 in libipset.list_entries(self.setname4))
            self.assertFalse(addr2 in libipset.list_entries(self.setname6))

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr2},
            )
            self.assertFalse(addr1 in libipset.list_entries(self.setname4))
            self.assertTrue(addr2 in libipset.list_entries(self.setname6))
