""" Clear entries management command module. """
from django.core.management.base import BaseCommand
from ipset.maintenance import clear_entries


class Command(BaseCommand):
    """ A management command to remove old entries from the project db. """

    help = (
        "Can be run as a cronjob or directly to clean out expired entries."
    )

    def handle(self, **options):
        """ Remove expired entries. """
        clear_entries()
