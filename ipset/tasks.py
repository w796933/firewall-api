""" Queue tasks module. """
import logging


def clean_blacklist():
    """ Clean the blacklist. """
    logging.getLogger('django.server').info('Clean blacklist')


def clean_whitelist():
    """ Clean the whitelist. """
    logging.getLogger('django.server').info('Clean whitelist')


def init_blacklist():
    """ Init the blacklist. """
    logging.getLogger('django.server').info('Init blacklist')


def init_whitelist():
    """ Init the whitelist. """
    logging.getLogger('django.server').info('Init whitelist')
