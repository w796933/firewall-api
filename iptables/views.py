""" iptables app views module. """
import ipaddress
from django.http import HttpResponseBadRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from iptables import libiptables


@method_decorator(csrf_exempt, name='dispatch')
class InputAcceptView(View):
    """ A POST-only endpoint to add or delete an iptables rule
    to accept IPv4 and IPv6 traffic. """

    http_method_names = ['post']

    @staticmethod
    def _exec(action, transport, start, end, src):
        """ Add or delete a rule. """
        protos = ['ipv4', 'ipv6']
        if src:
            try:
                ipaddress.IPv4Address(src)
            except ValueError:
                protos.remove('ipv4')
            try:
                ipaddress.IPv6Address(src)
            except ValueError:
                protos.remove('ipv6')
        for proto in protos:
            exists = libiptables.check_input_accept(
                proto, transport, start, end, src
            )
            if action == 'delete' and exists:
                libiptables.delete_input_accept(
                    proto, transport, start, end, src
                )
            elif action == 'add' and not exists:
                libiptables.add_input_accept(
                    proto, transport, start, end, src
                )

    @staticmethod
    def _get_data(request):
        """ Raise ValueError if there are any problems with the input data
        and return valid data. """

        # Marshal data.
        data = request.POST.dict()
        try:
            action = data['action']
            transport = data['transport']
            start = data['start']
            end = data['end']
            src = data.get('src')
        except KeyError as err:
            raise ValueError from err

        # Validate and return.
        if action not in ['add', 'delete']:
            raise ValueError('Bad action')
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
        if src:
            ipaddress.ip_address(src)
        return action, transport, range_start, range_end, src

    def post(self, request, *args, **kwargs):
        """ POST to add or delete INPUT ACCEPT rule. """
        # pylint: disable=unused-argument
        try:
            self._exec(*self._get_data(request))
            return HttpResponse()
        except ValueError as err:
            return HttpResponseBadRequest(str(err))
