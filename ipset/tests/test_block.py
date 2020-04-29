""" Blocked addresses test module. """
from django.core import mail
from ipset.tests.base import IpsetTestCase


class BlockTestCase(IpsetTestCase):
    """ Validate the block endpoint. """

    def test_not_implemented(self):
        """ Test any POST. """
        response = self.client.post(
            '/ipset/block',
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(mail.outbox) == 1)


class BlockInitTestCase(IpsetTestCase):
    """ Validate blocked addresses init. """


class BlockCleanTestCase(IpsetTestCase):
    """ Validate blocked addresses cleanup. """
