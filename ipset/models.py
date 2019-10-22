""" IP set models module. """
from datetime import timedelta
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils import timezone
from ipset import libipset


class Set(models.Model):
    """ A unique set name and a set of Entry objects. """

    name = models.CharField(
        max_length=12,
        unique=True,
        validators=(
            validators.validate_slug,
        ),
    )

    # self.entry_set.all()

    def proto_name(self, address):
        """ Return protocol-specific setname based on address type. """
        try:
            validators.validate_ipv4_address(address)
            return '%s4' % self.name
        except ValidationError:
            try:
                validators.validate_ipv6_address(address)
                return '%s6' % self.name
            except ValidationError:
                raise ValueError('Bad address')


def _new_expires():
    """ Return a datetime some time in the future. """
    return timezone.now() + timedelta(minutes=60)


class Entry(models.Model):
    """ A unique entry ID, an IPv4 or IPv6 address, the Sets the Entry
    is a member of, and an expiry datetime. """

    created = models.DateTimeField(
        auto_now_add=True,
    )
    address = models.GenericIPAddressField()
    entry_id = models.CharField(
        max_length=100,
        unique=True,
    )
    sets = models.ManyToManyField(
        Set,
    )
    expires = models.DateTimeField(
        default=_new_expires,
    )

    def advance(self):
        """ Advance expiry datetime. """
        self.expires = _new_expires()
        self.save()

    def init(self, *sets):
        """ Add entry's address to some or all of its sets. """
        if sets:
            init_sets = sets
        else:
            init_sets = self.sets.all()
        for _set in init_sets:
            libipset.add_entry(_set.proto_name(self.address), self.address)

    def purge(self, *sets):
        """ Remove entry's address from some or all of its sets and return
        the number of addresses removed. """

        def remove_entry(_set):
            """ Remove an entry from the underlying ipset and return True
            if the entry's address is removed from the set. """
            if self.address not in settings.IPSETS[_set.name]:
                entries = _set.entry_set.filter(address=self.address)
                if entries.count() == 1 and entries.first() == self:
                    libipset.remove_entry(
                        _set.proto_name(self.address), self.address
                    )
                    return True
            return False

        if sets:
            purge_sets = sets
        else:
            purge_sets = self.sets.all()
        removed = 0
        for _set in purge_sets:
            if remove_entry(_set):
                removed += 1
        return removed
