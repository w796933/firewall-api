""" A Python 3 module interface to manage iptables rules using iptables
and ip6tables command line tools. """
import logging
import subprocess
from subprocess import PIPE


logger = logging.getLogger('django.server')


def _get_command(transport, start, end, src):
    """ Get the command as an array. """
    # pylint: disable=unused-argument
    cmd = 'INPUT'
    if src:
        cmd += ' -s {src}/32'
    cmd += ' -p {transport}'
    if start == end:
        cmd += ' -m {transport} --dport {start}'
    else:
        cmd += ' -m multiport --dports {start}:{end}'
    cmd += ' -j ACCEPT'
    cmd = cmd.format(transport=transport, start=start, end=end, src=src)
    return cmd.split()


def _prepend_executable(ip_proto, cmd):
    """ Prepend iptables or ip6tables to the command. """
    if ip_proto == 'ipv4':
        cmd.insert(0, 'iptables')
    elif ip_proto == 'ipv6':
        cmd.insert(0, 'ip6tables')
    else:
        raise ValueError('Bad IP protocol')


def add_input_accept(ip_proto, transport, start, end, src=None):
    """ Add rule to accept traffic from a source address. """
    cmd = _get_command(transport, start, end, src)
    cmd.insert(0, '-A')
    _prepend_executable(ip_proto, cmd)
    logger.info(' '.join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        raise ValueError from err


def check_input_accept(ip_proto, transport, start, end, src=None):
    """ Check input accept rule. """
    cmd = _get_command(transport, start, end, src)
    cmd.insert(0, '-C')
    _prepend_executable(ip_proto, cmd)
    logger.info(' '.join(cmd))
    process = subprocess.run(cmd, check=False, stdout=PIPE, stderr=PIPE)
    return process.returncode == 0


def delete_input_accept(ip_proto, transport, start, end, src=None):
    """ Delete input accept rule. """
    cmd = _get_command(transport, start, end, src)
    cmd.insert(0, '-D')
    _prepend_executable(ip_proto, cmd)
    logger.info(' '.join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        raise ValueError from err
