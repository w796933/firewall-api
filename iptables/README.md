# App notes

This app provides
a POST-only HTTP interface
to add and remove iptables and ip6tables rules
that accept traffic to a single TCP or UDP port
or to a range of ports.

POSTing to the endpoint
adds and deletes iptables rules
for both IPv4 and IPv6 network stacks.

The app provides no model
to persist iptables rules,
only an API.

The `firewall-app` provides a method
that Django projects can use
to open service ports when the project starts.


## API endpoint

The app provides a single HTTP POST endpoint
at `input/accept`.

The endpoint takes
`action`, `transport`, `start` and `end` POST keys.
All keys are mandatory and validation errors raise 400.

- `action` must be either `add` or `delete`.
- `transport` must be either `tpc` or `udp`.
- `start` and `end` ports must be integers.
- The `start` port integer must be equal to or less than `end`.
- Both `start` and `end` must be unpriviledged ports
  in the range from 1024 to 65535.
