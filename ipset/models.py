""" IP set models module. """
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def is_ipv4(address):
    """ Return True if the address is IPv4. """
    try:
        validators.validate_ipv4_address(address)
        return True
    except ValidationError:
        return False


def is_ipv6(address):
    """ Return True if the address is IPv6. """
    try:
        validators.validate_ipv6_address(address)
        return True
    except ValidationError:
        return False


def setname(address, ipset):
    """ Return protocol-specific setname or raise ValueError. """
    if is_ipv4(address):
        return '%s4' % ipset
    if is_ipv6(address):
        return '%s6' % ipset
    raise ValueError('Bad address')


class AbstractAddress(models.Model):
    """ And IPv4 or IPv6 address. """

    class Meta:
        abstract = True

    address = models.GenericIPAddressField()


class BlockedAddress(AbstractAddress):
    """ An IPv4 or IPv6 address, a banned state
    and a set of block events. """

    banned = models.BooleanField()

    # self.blockevent_set.all()


class BlockEvent(models.Model):
    """ An address, a reason, a severity and a timeout. """

    address = models.ForeignKey(
        BlockedAddress,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    severity = models.SmallIntegerField()
    timeout = models.SmallIntegerField()
    reason = models.CharField(
        blank=True,
        max_length=32,
        validators=(
            validators.validate_slug,
        ),
    )


class AdminAddress(AbstractAddress):
    """ An address and a last access time. """

    last_access = models.DateTimeField(auto_now=True)
