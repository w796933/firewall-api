""" IP set views module. """
import json
from django import forms
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from ipset.models import Entry, Set


@method_decorator(csrf_exempt, name='dispatch')
class EntryView(View):
    """ PUT address in existing entry or create new entry, DELETE entry. """

    http_method_names = ['delete', 'put']

    class AddressForm(forms.Form):
        """ Address validatoin form. """
        address = forms.GenericIPAddressField()

    class EntryForm(forms.ModelForm):
        """ Entry validation form. """
        class Meta:
            """ Form field def. """
            model = Entry
            fields = ['entry_id', 'address']

    @staticmethod
    def _create_or_update(request):
        """ Create an entry if the entry ID doesn't yet exist,
        or update the entry's address if it does. Raise ValueError
        on validation problems. """
        try:
            data = json.loads(request.body.decode())
        except (TypeError, UnicodeError) as err:
            raise ValueError(str(err))
        try:
            entry_id = data['entry']
            address = data['address']
        except KeyError:
            raise ValueError('Bad data')
        if not EntryView.AddressForm({'address': address}).is_valid():
            raise ValueError('Bad address')
        try:
            entry = Entry.objects.get(entry_id=entry_id)
            if entry.address != address:
                entry.purge()
                entry.address = address
                entry.save()
                entry.init()
            entry.advance()
        except Entry.DoesNotExist:
            try:
                entry = EntryView.EntryForm({
                    'entry_id': entry_id,
                    'address': address,
                }).save()
                entry.init()
            except forms.ValidationError:
                raise ValueError('Bad data')

    @staticmethod
    def _purge_and_delete(request):
        """ Purge an entry's address from its sets and delete the entry. """
        try:
            data = json.loads(request.body.decode())
        except (TypeError, UnicodeError) as err:
            raise ValueError(str(err))
        try:
            entry_id = data['entry']
        except KeyError:
            raise ValueError('Bad data')
        try:
            entry = Entry.objects.get(entry_id=entry_id)
            entry.purge()
            entry.delete()
        except Entry.DoesNotExist:
            raise Http404

    # pylint: disable=unused-argument
    def delete(self, request, *args, **kwargs):
        """ DELETE an entry. """
        try:
            self._purge_and_delete(request)
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            raise SuspiciousOperation(str(err))

    # pylint: disable=unused-argument
    def put(self, request, *args, **kwargs):
        """ PUT an entry and its address. """
        try:
            self._create_or_update(request)
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            raise SuspiciousOperation(str(err))


@method_decorator(csrf_exempt, name='dispatch')
class SetView(View):
    """ PUT entry into set, DELETE entry from set. """

    http_method_names = ['delete', 'put']

    @staticmethod
    def _entry_set(request):
        """ Return entry and set from request data. """
        try:
            data = json.loads(request.body.decode())
        except (TypeError, UnicodeError) as err:
            raise ValueError(str(err))
        try:
            entry_id = data['entry']
            set_name = data['set']
        except KeyError:
            raise ValueError('Bad data')
        try:
            entry = Entry.objects.get(entry_id=entry_id)
        except Entry.DoesNotExist:
            raise Http404
        try:
            _set = Set.objects.get(name=set_name)
        except Set.DoesNotExist:
            raise ValueError('Bad set')
        return entry, _set

    # pylint: disable=unused-argument
    def delete(self, request, *args, **kwargs):
        """ Remove an entry from a set. """
        try:
            entry, _set = self._entry_set(request)
            if not _set.entry_set.filter(entry_id=entry.entry_id).exists():
                raise ValueError('Bad entry')
            entry.purge(_set)
            entry.sets.remove(_set)
            if entry.sets.count() == 0:
                entry.delete()
            # Don't advance entry expiry if the entry still exists.
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            raise SuspiciousOperation(str(err))

    # pylint: disable=unused-argument
    def put(self, request, *args, **kwargs):
        """ Add an entry to a set. """
        try:
            entry, _set = self._entry_set(request)
            entry.sets.add(_set)
            entry.init(_set)
            entry.advance()
            return JsonResponse({}, **kwargs)
        except ValueError as err:
            raise SuspiciousOperation(str(err))
