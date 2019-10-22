""" Test module for basic entry put, set put and set delete. """
from ipset import libipset
from ipset.maintenance import clear_entries
from ipset.models import Entry
from ipset.tests.base import IpsetTestCase


class ClearTestCase(IpsetTestCase):
    """ Validate basic entry creation and deletion. """

    def test_clear(self):
        """ Assert that an address is removed from the underlying
        set when entries are cleared. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            from datetime import timedelta
            from django.utils import timezone
            from freezegun import freeze_time

            freezer = freeze_time(timezone.now() - timedelta(days=1))
            freezer.start()
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
            freezer.stop()

            clear_entries()
            self.assertFalse(libipset.test_entry(self.setname4, addr))

            with self.assertRaisesMessage(Entry.DoesNotExist, ''):
                Entry.objects.get(entry_id=entry_id)

    def test_clear_multiple(self):
        """ Assert that an address in multiple entries is removed
        from the underlying set when entries are cleared. """
        addr = '10.10.10.10'
        entry1_id = 'hi1'
        entry2_id = 'hi2'
        with self.settings(IPSETS={self.setname: []}):
            from datetime import timedelta
            from django.utils import timezone
            from freezegun import freeze_time

            freezer = freeze_time(timezone.now() - timedelta(days=1))
            freezer.start()
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry1_id, 'address': addr},
            )
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry1_id, 'set': self.setname},
            )
            self.assertTrue(libipset.test_entry(self.setname4, addr))
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry2_id, 'address': addr},
            )
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry2_id, 'set': self.setname},
            )
            self.assertTrue(libipset.test_entry(self.setname4, addr))
            freezer.stop()

            clear_entries()
            self.assertFalse(libipset.test_entry(self.setname4, addr))

            with self.assertRaisesMessage(Entry.DoesNotExist, ''):
                Entry.objects.get(entry_id=entry1_id)
            with self.assertRaisesMessage(Entry.DoesNotExist, ''):
                Entry.objects.get(entry_id=entry2_id)
