""" Queue tasks module. """
import logging


def clean_blacklist():
    """ Clean the blacklist. """
    logging.getLogger('django.server').info('Clean blacklist')


def clean_whitelist():
    """ Clean the whitelist. """
    logging.getLogger('django.server').info('Clean whitelist')
