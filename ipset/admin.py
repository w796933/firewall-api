""" Ipset admin module. """
from django.contrib import admin
from ipset.models import Entry, Set


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    """ Set admin tweaks. """

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """ Entry admin tweaks. """

    list_display = (
        'entry_id',
        'address',
        'created',
        'expires',
    )

    def has_add_permission(self, request):
        """ Disable add. """
        return False

    def has_change_permission(self, request, obj=None):
        """ Disable change. """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Disable delete. """
        return False
