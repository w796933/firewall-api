""" IP set views module. """
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from ipset import libipset
from ipset.models import setname, AdminAddress


@method_decorator(csrf_exempt, name='dispatch')
class AdminView(View):
    """ Admin endpoint POST view. """

    http_method_names = ['post']

    # pylint: disable=unused-argument
    def post(self, request, *args, **kwargs):
        """ Process POST data. """
        data = request.POST.dict()
        try:
            address = data['address']
            ipset = setname(address, 'admin')
            if libipset.test_entry(ipset, address):

                # The address is in the ipset. Save and return.
                try:
                    AdminAddress.objects.get(address=address).save()
                except AdminAddress.DoesNotExist:
                    pass
                return HttpResponse()

            # The object is not in db or ipset. Add and return.
            AdminAddress.objects.create(address=address)
            libipset.add_entry(ipset, address)
            return HttpResponse()
        except (KeyError, ValueError) as err:
            raise SuspiciousOperation(str(err))


@method_decorator(csrf_exempt, name='dispatch')
class BlockView(View):
    """ Block endpoint POST view. """

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        """ Process POST data. """
        raise SuspiciousOperation('Not implemented')
