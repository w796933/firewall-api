""" Test module for EntryView PUT. """
from ipset.models import Entry
from ipset.tests.base import IpsetTestCase
from ipset import libipset
from ipset.maintenance import sync


class EntryViewDelTestCase(IpsetTestCase):
    """ Validate entry view DELETE. """

    def test_bad_entry(self):
        """ Assert that DELETE of non-existent entry raises 404. """
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            response = self.client.delete(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id},
            )
            self.assertEqual(response.status_code, 404)

    def test_delete_object(self):
        """ Assert that DELETE removes the entry object from the db. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            self.client.delete(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id},
            )
            with self.assertRaisesMessage(Entry.DoesNotExist, ''):
                Entry.objects.get(entry_id=entry_id)

    def test_delete_default(self):
        """ Assert that DELETE of default address leaves it in the set. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: [addr]}):
            sync()  # Note.
            self.assertTrue(libipset.test_entry(self.setname4, addr))
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            self.client.delete(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id},
            )
            self.assertTrue(libipset.test_entry(self.setname4, addr))
