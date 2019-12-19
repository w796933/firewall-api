""" Test module for SetView DELETE. """
from django.core import mail
from ipset.models import Entry
from ipset.tests.base import IpsetTestCase, TwoIpsetTestCase
from ipset import libipset


class SetViewDeleteTestCase(IpsetTestCase):
    """ Validate set view DELETE. """

    def test_bad_entry(self):
        """ Assert that DELETE of non-existent entry raises 404. """
        entry_id = 'hi'
        with self.settings(IPSETS={self.setname: []}):
            response = self.client.delete(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            self.assertEqual(response.status_code, 404)

    def test_bad_set(self):
        """ Assert that DELETE of non-existent set raises 400. """
        addr = '10.10.10.10'
        entry_id = 'hi'
        bad_set = 'badset'
        with self.settings(IPSETS={self.setname: []}):
            self.client.put(
                '/ipset/entry/',
                content_type='application/json',
                data={'entry': entry_id, 'address': addr},
            )
            response = self.client.delete(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': bad_set},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.context['exception_value'], 'Bad set')
            self.assertTrue('Bad set' in mail.outbox[0].subject)

    def test_delete_entry(self):
        """ Assert that DELETE of of last set deletes entry record. """
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
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.sets.count() == 1)
            self.client.delete(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            with self.assertRaisesMessage(Entry.DoesNotExist, ''):
                Entry.objects.get(entry_id=entry_id)


# pylint: disable=too-many-ancestors
class SetViewDeleteTwoIpsetTestCase(TwoIpsetTestCase):
    """ Validate set view DELETE with more than one ipset. """

    def test_sets(self):
        """ Assert that both sets exist. """
        with self.settings(IPSETS={self.setname: []}):
            sets = libipset.list_sets()
            self.assertTrue(self.setname4 in sets)
            self.assertTrue(self.setname6 in sets)
            self.assertTrue(self.setname_b4 in sets)
            self.assertTrue(self.setname_b6 in sets)

    def test_is_not_in_set(self):
        """ Assert that DELETE a set of set the entry isn't in raises 400. """
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
            response = self.client.delete(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname_b},
            )
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.context['exception_value'], 'Bad entry')
            self.assertTrue('Bad entry' in mail.outbox[0].subject)

    def test_delete_entry(self):
        """ Assert that DELETE of of last set deletes entry record. """
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
            self.client.put(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname_b},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.sets.count() == 2)
            self.client.delete(
                '/ipset/set/',
                content_type='application/json',
                data={'entry': entry_id, 'set': self.setname},
            )
            entry = Entry.objects.get(entry_id=entry_id)
            self.assertTrue(entry.sets.count() == 1)
