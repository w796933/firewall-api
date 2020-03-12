""" Test module for InputAcceptView. """
from iptables.tests.base import IptablesTestCase


class InputAcceptTests(IptablesTestCase):
    """ Validate basic rule addition and deletion. """

    def test_tcp_port(self):
        """ Assert that iptables rules are added for a single tcp port. """
        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'add',
                'transport': 'tcp',
                'start': 8443,
                'end': 8443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'add',
                'transport': 'tcp',
                'start': 8443,
                'end': 8443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'delete',
                'transport': 'tcp',
                'start': 8443,
                'end': 8443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'delete',
                'transport': 'tcp',
                'start': 8443,
                'end': 8443
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_udp_port_range(self):
        """ Assert that iptables rules are added for a udp port range. """
        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'add',
                'transport': 'udp',
                'start': 8443,
                'end': 9443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'add',
                'transport': 'udp',
                'start': 8443,
                'end': 9443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'delete',
                'transport': 'udp',
                'start': 8443,
                'end': 9443
            },
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            '/iptables/input/accept',
            data={
                'action': 'delete',
                'transport': 'udp',
                'start': 8443,
                'end': 9443
            },
        )
        self.assertEqual(response.status_code, 200)
