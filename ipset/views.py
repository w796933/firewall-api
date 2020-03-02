""" IP set views module. """
import json
from django import forms
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
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


@method_decorator(csrf_exempt, name='dispatch')
class BlacklistView(View):
    """ Blacklist POST view. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Process blacklist POST data. """
        data = request.POST.dict()
