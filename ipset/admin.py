""" Ipset admin module. """
from django.contrib import admin
from ipset.models import BlockedAddress, BlockEvent, AdminAddress


@admin.register(BlockedAddress)
class BlockedAddressAdmin(admin.ModelAdmin):
    """ BlockedAddress admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(BlockEvent)
class BlockEventAdmin(admin.ModelAdmin):
    """ BlockEvent admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(AdminAddress)
class AdminAddressAdmin(admin.ModelAdmin):
    """ AdminAddress admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False
