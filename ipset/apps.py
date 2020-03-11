""" Ipset apps module. """
import sys
from django.apps import AppConfig


CLEAN_MINUTES = 1


class IpsetConfig(AppConfig):
    """ Ipset app config. """
    name = 'ipset'
    verbose_name = 'IP set'

    @staticmethod
    def schedule_clean(name, func, minutes):
        """ Add or update a scheduled ipset clean function. """
        # pylint: disable=import-outside-toplevel
        from datetime import timedelta
        from django.utils import timezone
        from django_q.models import Schedule
        from django_q.tasks import schedule

        try:
            obj = Schedule.objects.get(name=name)
            obj.next_run = timezone.now() + timedelta(minutes=minutes)
            obj.minutes = minutes
            obj.save()
        except Schedule.DoesNotExist:
            schedule(
                func,
                name=name,
                schedule_type=Schedule.MINUTES,
                minutes=minutes,
                next_run=(timezone.now() + timedelta(minutes=minutes))
            )

    def ready(self):
        """ Schedule clean tasks when the app is started by django-q,
        and run init when the app starts as an ASGI application. """

        # Schedule clean tasks on queue cluster start.
        if sys.argv[-1] == 'qcluster':
            IpsetConfig.schedule_clean(
                'clean-blacklist',
                'ipset.tasks.clean_blacklist',
                CLEAN_MINUTES,
            )
            IpsetConfig.schedule_clean(
                'clean-whitelist',
                'ipset.tasks.clean_whitelist',
                CLEAN_MINUTES,
            )

        # Run init methods on application start.
        if sys.argv[-1] == 'project.asgi:application':
            # pylint: disable=import-outside-toplevel
            from ipset.init import init_blacklist, init_whitelist

            init_blacklist()
            init_whitelist()
