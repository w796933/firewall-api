""" iptables app views module. """
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from iptables import libiptables


@method_decorator(csrf_exempt, name='dispatch')
class InputAcceptView(View):
    """ A POST-only endpoint to add or delete an iptables rule
    to accept IPv4 and IPv6 traffic for either tcp or udp transport
    for a range of ports from start to end. To enable a single port,
    start == end. """

    http_method_names = ['post']

    @staticmethod
    def _add_rule(transport, start, end):
        """ Add a rule. """
        ipv4_exists = libiptables.check_input_accept(
            'ipv4', transport, start, end
        )
        if not ipv4_exists:
            libiptables.add_input_accept('ipv4', transport, start, end)
        ipv6_exists = libiptables.check_input_accept(
            'ipv6', transport, start, end
        )
        if not ipv6_exists:
            libiptables.add_input_accept('ipv6', transport, start, end)

    @staticmethod
    def _delete_rule(transport, start, end):
        """ Delete a rule. """
        ipv4_exists = libiptables.check_input_accept(
            'ipv4', transport, start, end
        )
        if ipv4_exists:
            libiptables.delete_input_accept('ipv4', transport, start, end)
        ipv6_exists = libiptables.check_input_accept(
            'ipv6', transport, start, end
        )
        if ipv6_exists:
            libiptables.delete_input_accept('ipv6', transport, start, end)

    @staticmethod
    def _get_data(request):
        """ Raise ValueError if there are any problems with the input data
        and return a three-tuple of validated transport and start/end
        ports as integers. """

        # Marshal data.
        data = request.POST.dict()
        try:
            action = data['action']
            transport = data['transport']
            start = data['start']
            end = data['end']
        except KeyError:
            raise ValueError('Bad data')

        # Validate and return.
        range_start = int(start)
        range_end = int(end)
        if transport not in ('tcp', 'udp'):
            raise ValueError('Bad transport')
        if range_start > range_end:
            raise ValueError('Bad start port')
        if range_start < 1024 or range_start > 65535:
            raise ValueError('Bad start port range')
        if range_end < 1024 or range_end > 65535:
            raise ValueError('Bad end port range')
        return action, transport, range_start, range_end

    def post(self, request, *args, **kwargs):
        """ POST to add or delete INPUT ACCEPT rule. """
        # pylint: disable=unused-argument
        try:
            action, transport, start, end = self._get_data(request)
            if action == 'add':
                self._add_rule(transport, start, end)
            elif action == 'delete':
                self._delete_rule(transport, start, end)
            else:
                raise ValueError('Bad action')
            return HttpResponse()
        except ValueError as err:
            return HttpResponseBadRequest(str(err))
