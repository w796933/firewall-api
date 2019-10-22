""" A Python 3 module interface to manage iptables rules using iptables
and ip6tables command line tools. """
import logging
import subprocess
from subprocess import PIPE


def _get_command(transport, start, end):
    """ Get the command as an array. """
    if start == end:
        cmd = 'INPUT -p %s -m %s --dport %i -j ACCEPT' % (
            transport, transport, start
        )
        return cmd.split()
    cmd = 'INPUT -p %s -m multiport --dports %i:%i -j ACCEPT' % (
        transport, start, end
    )
    return cmd.split()


def _prepend_executable(ip_proto, cmd):
    """ Prepend iptables or ip6tables to the command. """
    if ip_proto == 'ipv4':
        cmd.insert(0, 'iptables')
    elif ip_proto == 'ipv6':
        cmd.insert(0, 'ip6tables')
    else:
        raise ValueError('Bad IP protocol')


def add_input_accept(ip_proto, transport, start, end):
    """ Run an iptables command to add an INPUT ACCEPT rule for
    udp/tdp transport access to a port range of start/end. """
    cmd = _get_command(transport, start, end)
    cmd.insert(0, '-A')
    _prepend_executable(ip_proto, cmd)
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    logging.getLogger('django.server').info(
        'Add %s INPUT ACCEPT %s %s:%s', ip_proto, transport, start, end,
    )


def check_input_accept(ip_proto, transport, start, end):
    """ Run an iptables command to check an INPUT ACCEPT rule for
    udp/tdp transport access to a port range of start/end and return True
    if the rule exists, or False. """
    cmd = _get_command(transport, start, end)
    cmd.insert(0, '-C')
    _prepend_executable(ip_proto, cmd)
    process = subprocess.run(cmd, check=False, stdout=PIPE, stderr=PIPE)
    return process.returncode == 0


def delete_input_accept(ip_proto, transport, start, end):
    """ Run an iptables command to delete an INPUT ACCEPT rule for
    udp/tdp transport access to a port range of start/end. """
    cmd = _get_command(transport, start, end)
    cmd.insert(0, '-D')
    _prepend_executable(ip_proto, cmd)
    try:
        subprocess.run(cmd, check=True, stdout=PIPE, stderr=PIPE)
    except subprocess.CalledProcessError as err:
        print(err)
        raise ValueError(err.stderr)
    logging.getLogger('django.server').info(
        'Delete %s INPUT ACCEPT %s %s:%s', ip_proto, transport, start, end,
    )
