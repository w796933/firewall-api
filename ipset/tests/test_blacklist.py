""" Blacklist test module. """
from django.core import mail
from ipset.tests.base import IpsetTestCase


class BlacklistTestCase(IpsetTestCase):
    """ Validate the ipset blacklist API. """

    def test_not_implemented(self):
        """ Test any POST. """
        response = self.client.post(
            '/ipset/blacklist',
            HTTP_X_FORWARDED_HOST='localhost',
        )
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(mail.outbox) == 1)


class BlacklistInitTestCase(IpsetTestCase):
    """ Validate ipset blacklist init. """


class BlacklistCleanTestCase(IpsetTestCase):
    """ Validate ipset blacklist clean. """
