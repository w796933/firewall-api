""" A Python 3 module interface to manage entries in underlying ipsets
using the ipset command line tool.

Create and destroy underlying ipsets using config mangagement. This module
only adds, removes, tests and lists.

This is a very naive implementation, but it works, and it seems safe (!)
and simple to me, if perhaps not performant.
"""
import logging
import subprocess
from subprocess import PIPE


def add_entry(setname, entry):
    """ Add entry to underlying ipset. Allow if entry already in set. """
    cmd = ['ipset', '-exist', 'add', setname, entry]
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    logging.getLogger('django.server').info(
        'Added %s to %s', entry, setname
    )


def list_entries(setname):
    """ Return list of entries in ipset. """
    cmd = ['ipset', 'list', setname, '-o', 'save']
    try:
        result = subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    entries = []
    for line in result.stdout.decode().splitlines():
        if line.startswith('add '):
            entries.append(line.split()[-1])
    return entries


def list_sets():
    """ Return list of existing ipsets. """
    cmd = ['ipset', 'list', '-name']
    try:
        result = subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    return result.stdout.decode().splitlines()


def remove_entry(setname, entry):
    """ Remove entry from underlying ipset. Allow if entry not in set. """
    cmd = ['ipset', '-exist', 'del', setname, entry]
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    logging.getLogger('django.server').info(
        'Removed %s from %s', entry, setname
    )


def test_entry(setname, entry):
    """ Test that entry is in ipset. """
    cmd = ['ipset', 'test', setname, entry]
    try:
        result = subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        if 'is NOT in set' in str(err.stderr):
            return False
        print(result)
        raise ValueError(result.stderr)
    return True
