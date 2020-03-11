""" IP set views module. """
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from ipset import libipset
from ipset.models import (
    setname,
    WhitelistAddress,
)


@method_decorator(csrf_exempt, name='dispatch')
class WhitelistView(View):
    """ Whitelist POST view. """

    http_method_names = ['post']

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """ Process whitelist POST data. """
        data = request.POST.dict()
        try:
            address = data['address']
            ipset = setname(address, 'whitelist')
            if libipset.test_entry(ipset, address):

                # The address is in the ipset. Save and return.
                try:
                    WhitelistAddress.objects.get(address=address).save()
                except WhitelistAddress.DoesNotExist:
                    pass
                return HttpResponse()

            # The object is not in db or ipset. Add and return.
            WhitelistAddress.objects.create(address=address)
            libipset.add_entry(ipset, address)
            return HttpResponse()
        except (KeyError, ValueError) as err:
            raise SuspiciousOperation(str(err))


@method_decorator(csrf_exempt, name='dispatch')
class BlacklistView(View):
    """ Blacklist POST view. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Process blacklist POST data. """
        raise SuspiciousOperation('Not implemented')
