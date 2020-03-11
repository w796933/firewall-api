""" Blacklist/whitelist init functions module. """
import logging


def init_blacklist():
    """ Init blacklist on start. """
    logging.getLogger('django.server').info('Init blacklist')


def init_whitelist():
    """ Init whitelist on start. """
    logging.getLogger('django.server').info('Init whitelist')
