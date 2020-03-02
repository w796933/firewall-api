""" Ipset admin module. """
from django.contrib import admin
from ipset.models import (
    BlacklistAddress,
    BlacklistEvent,
    WhitelistAddress,
)


@admin.register(BlacklistAddress)
class BlacklistAddressAdmin(admin.ModelAdmin):
    """ BlacklistAddress admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(BlacklistEvent)
class BlacklistEventAdmin(admin.ModelAdmin):
    """ BlacklistEvent admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(WhitelistAddress)
class WhitelistAddressAdmin(admin.ModelAdmin):
    """ WhitelistAddress admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False
