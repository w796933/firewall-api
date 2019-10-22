""" Maintenance methods. """
import logging
from django.conf import settings
from django.core import validators
from django.forms import ModelForm, ValidationError
from django.utils import timezone
from ipset import libipset
from ipset.models import Entry, Set


def _sync_objects_to_kernel(set_name, defaults):
    """ Add and remove addresses in underlying sets to sync actual set
    membership with default and session addresses. """

    def get_set(address, set4, set6):
        """ Return the correct set based on addr, or raise ValueError. """
        try:
            validators.validate_ipv4_address(address)
            return set4
        except ValidationError:
            try:
                validators.validate_ipv6_address(address)
                return set6
            except ValidationError:
                raise ValueError('Bad address')

    # Initialize sets from libipset and settings.
    setname4 = '%s4' % set_name
    setname6 = '%s6' % set_name
    current4 = set(libipset.list_entries(setname4))
    current6 = set(libipset.list_entries(setname6))
    required4 = set()
    required6 = set()
    if defaults:
        for addr in defaults:
            get_set(addr, required4, required6).add(addr)

    # Initialize sets from session records.
    remove4 = current4 - required4
    remove6 = current6 - required6
    entries = Set.objects.get(name=set_name).entry_set.all()
    for entry in entries:
        get_set(entry.address, required4, required6).add(entry.address)
        remove = get_set(entry.address, remove4, remove6)
        if entry.address in remove:
            remove.remove(entry.address)

    # Sync initialized sets to kernel.
    for addr in required4 - current4:
        libipset.add_entry(setname4, addr)
    for addr in remove4:
        libipset.remove_entry(setname4, addr)
    for addr in required6 - current6:
        libipset.add_entry(setname6, addr)
    for addr in remove6:
        libipset.remove_entry(setname6, addr)


def clear_entries():
    """ Clear expired entries from the project database. """
    deleted = 0
    removed = 0
    for entry in Entry.objects.filter(expires__lt=timezone.now()):
        removed += entry.purge()
        _, objects = entry.delete()
        if 'ipset.Entry' in objects:
            deleted += objects['ipset.Entry']
    logging.getLogger('django.server').info(
        'Deleted %s entries and %s addresses', deleted, removed,
    )


def sync():
    """ Sync project settings to db state and sync settings and db state
    to actual set membership. Raise ValueError when an ipset in settings
    doesn't exist on the host, and when libipset commands fail. """

    class SetForm(ModelForm):
        """ Set validation form. """
        class Meta:
            """ Form field def. """
            model = Set
            fields = ['name']

    # Delete Set objects that are not in settings.
    for _set in Set.objects.all():
        if _set.name not in settings.IPSETS:
            _set.delete()

    # Create missing Set objects.
    for set_name in settings.IPSETS.keys():
        try:
            Set.objects.get(name=set_name)
        except Set.DoesNotExist:
            try:
                SetForm({'name': set_name}).save()
            except ValidationError:
                raise ValueError('Bad set')

    # Sync settings/db data to kernel sets.
    for set_name, defaults in settings.IPSETS.items():
        _sync_objects_to_kernel(set_name, defaults)
