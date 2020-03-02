""" Ipset middleware module. """
import sys
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import schedule


class ScheduleMiddleware:  # pylint: disable=too-few-public-methods
    """ Schedule init/cleanup tasks. """

    @staticmethod
    def schedule_cleanup(name, func, minutes):
        """ Add or update a scheduled cleanup function. """
        try:
            obj = Schedule.objects.get(name=name)
            if obj.minutes != minutes:
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

    @staticmethod
    def schedule_init(name, func):
        """ Add an init function. """
        try:
            Schedule.objects.get(name=name)
        except Schedule.DoesNotExist:
            schedule(
                func,
                name=name,
                schedule_type=Schedule.ONCE,
                next_run=timezone.now()
            )

    def __init__(self, get_response):
        """ Schedule tasks and remove the middleware when complete. """

        # Middleware runs on start, but not by management commands,
        # and I'm pretty sure not by tests.

        # Remove middleware based on command line.
        if ':application' not in sys.argv[-1]:
            raise MiddlewareNotUsed('Scheduling aborted')

        # Schedule init and cleanup tasks.
        ScheduleMiddleware.schedule_init(
            'init-blacklist',
            'ipset.tasks.init_blacklist',
        )
        ScheduleMiddleware.schedule_init(
            'init-whitelist',
            'ipset.tasks.init_whitelist',
        )
        ScheduleMiddleware.schedule_cleanup(
            'clean-blacklist',
            'ipset.tasks.clean_blacklist',
            settings.CLEANUP_MINUTES,
        )
        ScheduleMiddleware.schedule_cleanup(
            'clean-whitelist',
            'ipset.tasks.clean_whitelist',
            settings.CLEANUP_MINUTES,
        )

        # Remove middleware after the first run.
        raise MiddlewareNotUsed('Scheduling complete')
