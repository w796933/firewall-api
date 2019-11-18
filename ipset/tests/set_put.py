""" Test module for SetView PUT. """
from django.core import mail
from ipset.models import Entry
from ipset.tests.base import IpsetTestCase
from ipset import libipset


class SetViewPutTestCase(IpsetTestCase):
    """ Validate set view PUT. """

    def test_bad_entry(self):
        """ Assert that PUT of non-existent entry raises 404. """
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            response = self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            self.assertEqual(response.status_code, 404)

    def test_bad_set(self):
        """ Assert that PUT of non-existent set raises 400. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        bad_set = 'badset'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            response = self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': bad_set},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.context['exception_value'], 'Bad set')
            self.assertTrue('Bad set' in mail.outbox[0].subject)

    def test_ipv4_entry(self):
        """ Assert that PUT adds the address to the IPv4 ipset. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            self.assertTrue(libipset.test_entry(self.setname4, addr))

    def test_ipv6_entry(self):
        """ Assert that PUT adds the address to the IPv6 ipset. """
        addr = 'fda3:9214:f305:abf7::1'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):

            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            self.assertTrue(libipset.test_entry(self.setname6, addr))

    def test_advance_expires(self):
        """ Assert expiry advances on PUT. """
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
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(old_expiry < entry.expires)

    def test_re_put_advance_expires(self):
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
            entry_put_expires = entry.expires

            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            set_put_expires = entry.expires
            self.assertTrue(entry_put_expires < set_put_expires)

            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            set_re_put_expires = entry.expires
            self.assertTrue(set_put_expires < set_re_put_expires)
