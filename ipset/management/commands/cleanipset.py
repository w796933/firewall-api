""" Clean entries managment command module. """
from django.core.management.base import BaseCommand
from ipset.clean import clean_admin_addrs


class Command(BaseCommand):
    """ A management command to remove old entries from the project db. """

    help = (
        "Can be run as a cronjob or directly to clean expired entries."
    )

    def handle(self, *args, **options):
        """ Remove expired entries. """
        clean_admin_addrs()
