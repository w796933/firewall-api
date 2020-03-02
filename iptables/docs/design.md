# Design notes

The iptables app provides
a JSON interface
to add iptables and ip6tables rules
to accept traffic to a single TCP or UDP port
or from a range of TCP or UDP ports.

Other services use this API
to open service ports
when they start.

The app provides no model
to persist iptables rules,
only an API.

## API endpoints

The app provides DELETE, GET and PUT endpoints,
but only PUT is used in practice.

All endpoints take a transport string (tcp or udp),
a start port, and an end port as input.

End port
must be specified,
start and end ports
must be integers,
and the start port
must be equal to or less than the end port.

Both start and end ports
must be valid unpriviledged ports
in the range from 1024 to 65535.

Validation errors raise 400.

### /iptables/input/accept/ DELETE

Delete iptables and ip6tables rules
if they exist,
or do nothing if one or both don't exist
and returns 200.

### /iptables/input/accept/ GET

Return 200 if both iptables and ip6tables rules exist,
or 404 if either is missing.

### /iptables/input/accept/ PUT

Add iptables and ip6tables rules
if either doesn't exist
and return 200
whether either rule is added or not.

## Stack common app

The stack-common app
provides a method
to call the PUT endpoint.

Projects that use the stack-common app
can open service ports
when the project starts
by importing the stack-common firewall module
and calling the iptables PUT method
on app ready.
