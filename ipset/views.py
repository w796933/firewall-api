""" IP set views module. """
from django import forms
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from ipset import libipset
from ipset.models import (
    BlacklistAddress,
    BlacklistEvent,
    WhitelistAddress,
)


@method_decorator(csrf_exempt, name='dispatch')
class WhitelistView(View):
    """ Whitelist POST view. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Process whitelist POST data. """
        data = request.POST.dict()
        try:
            address = data['address']
            obj, created = WhitelistAddress.objects.get_or_create(
                address=address,
            )
            if created and not libipset.test_entry(obj.setname(), address):
                libipset.add_entry(obj.setname(), address)
            if not created:
                obj.save()
            return HttpResponse()
        except (KeyError, ValueError) as err:
            raise SuspiciousOperation(str(err))


@method_decorator(csrf_exempt, name='dispatch')
class BlacklistView(View):
    """ Blacklist POST view. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Process blacklist POST data. """
        data = request.POST.dict()
