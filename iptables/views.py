""" iptables app views module. """
import json
from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from iptables import libiptables


@method_decorator(csrf_exempt, name='dispatch')
class InputAcceptView(View):
    """ DELETE/GET/PUT an iptables rule to accept IPv4 and IPv6 traffic
    for either tcp or udp transport for a range of ports from start to end.
    To enable a single port, start == end. """

    http_method_names = ['delete', 'get', 'put']

    def delete(self, request, *args, **kwargs):
        """ DELETE INPUT ACCEPT rule. """
        try:
            transport, start, end = self._get_data(request)
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
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            return HttpResponseBadRequest(str(err))

    def get(self, request, *args, **kwargs):
        """ GET INPUT ACCEPT, return 200 or 404 if either IPv4 or IPv6
        rules don't exist. """
        try:
            transport, start, end = self._get_data(request)
            ipv4_exists = libiptables.check_input_accept(
                'ipv4', transport, start, end
            )
            ipv6_exists = libiptables.check_input_accept(
                'ipv6', transport, start, end
            )
            if ipv4_exists and ipv6_exists:
                return JsonResponse({}, **kwargs)
            return Http404
        except ValueError as err:
            return HttpResponseBadRequest(str(err))

    def put(self, request, *args, **kwargs):
        """ PUT INPUT ACCEPT rule. """
        try:
            transport, start, end = self._get_data(request)
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
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            return HttpResponseBadRequest(str(err))

    @staticmethod
    def _get_data(request):
        """ Raise ValueError if there are any problems with the input data
        and return a three-tuple of validated transport and start/end
        ports as integers. """

        # Marshal data.
        try:
            data = json.loads(request.body.decode())
        except (TypeError, UnicodeError) as err:
            raise ValueError(str(err))
        try:
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
        return transport, range_start, range_end
