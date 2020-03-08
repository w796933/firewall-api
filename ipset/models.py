""" IP set models module. """
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


class AbstractAddress(models.Model):
    """ And IPv4 or IPv6 address. """

    class Meta:
        abstract = True

    address = models.GenericIPAddressField()
    ipsetname = None

    def is_ipv4(self):
        """ Return True if the address is IPv4. """
        try:
            validators.validate_ipv4_address(self.address)
            return True
        except ValidationError:
            return False

    def is_ipv6(self):
        """ Return True if the address is IPv6. """
        try:
            validators.validate_ipv6_address(self.address)
            return True
        except ValidationError:
            return False

    def setname(self):
        """ Return protocol-specific setname or raise ValueError. """
        if not self.ipsetname:
            raise ValueError('No setname')
        if self.is_ipv4():
            return '%s4' % self.ipsetname
        if self.is_ipv6():
            return '%s6' % self.ipsetname
        raise ValueError('Bad address')


class BlacklistAddress(AbstractAddress):
    """ An IPv4 or IPv6 address, a banned state
    and a set of blacklist events. """

    ipsetname = 'blacklist'
    banned = models.BooleanField()

    # self.blacklistevent_set.all()


class BlacklistEvent(models.Model):
    """ An address, a reason, a severity and a timeout. """

    address = models.ForeignKey(
        BlacklistAddress,
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


class WhitelistAddress(AbstractAddress):
    """ An address and a last access time. """

    ipsetname = 'whitelist'
    last_access = models.DateTimeField(auto_now=True)
